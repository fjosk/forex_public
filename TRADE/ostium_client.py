#!/usr/bin/env python3
"""
Ostium SDK client wrapper -- the ONE place the live/testnet trader touches ostium-python-sdk.

Thin, mode-parameterized layer over OstiumSDK so ostium_trader stays SDK-detail-free. Imports ONLY
from shared/ (instruments, ostium_data) -- never from LAB/. Runs in FOREX/.venv (the dedicated
ostium-python-sdk venv), NOT global-venv.

VERIFIED against ostium-python-sdk v3.2.1 (2026-06-07):
  OstiumSDK(network, private_key, rpc_url, verbose=False, use_delegation=False)
    .w3                       web3 instance
    .balance.get_usdc_balance(addr) / get_ether_balance(addr)
    .faucet.request_tokens()  testnet only -- sends an on-chain tx (NEEDS GAS), mints tokenAmount
                              (10,000 test USDC/request); .get_token_amount(), .can_request_tokens(addr)
    .subgraph.get_pairs()     name->id map (TESTNET ids differ from mainnet -- resolve at runtime)
    .ostium.set_slippage_percentage(pct)
    .ostium.perform_trade(trade_params, at_price)   open; approves USDC internally
    .ostium.close_trade(pair_id, trade_index, market_price, close_percentage=100)
    .ostium.update_sl(pairID, index, sl) / update_tp(pair_id, trade_index, tp_price)
  trade_params = {collateral(USDC float), leverage(float), asset_type(int pair_id),
                  direction(bool buy), tp(price or 0), sl(price or 0), order_type='MARKET'}

NETWORK: testnet = Arbitrum Sepolia (chainId 421614); RPC from env OSTIUM_SEPOLIA_RPC or the public
default. Key from env HL_TESTNET_PRIVATE_KEY (the existing wallet <testnet-wallet>; reused for TESTNET only
-- a dedicated wallet is the rule before mainnet, per FOREX/CLAUDE.md pre-deploy checklist).
"""
from __future__ import annotations

import asyncio
import inspect
import os
import sys
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # FOREX root for shared.*

from shared import instruments as _instr     # noqa: E402

DEFAULT_TESTNET_RPC = "https://sepolia-rollup.arbitrum.io/rpc"
DEFAULT_MAINNET_RPC = "https://arb1.arbitrum.io/rpc"
USDC_DECIMALS = 6


class OstiumClient:
    """Mode-parameterized Ostium SDK handle. mode in {'testnet','live'} (paper never builds this)."""

    def __init__(self, mode="testnet", verbose=False):
        from ostium_python_sdk import OstiumSDK, NetworkConfig
        self.mode = mode
        key = os.environ.get("HL_TESTNET_PRIVATE_KEY") if mode == "testnet" else \
            (os.environ.get("OSTIUM_MAINNET_PRIVATE_KEY") or os.environ.get("HL_TESTNET_PRIVATE_KEY"))
        if not key:
            raise RuntimeError("no private key in env (HL_TESTNET_PRIVATE_KEY)")
        if mode == "testnet":
            net = NetworkConfig.testnet()
            rpc = os.environ.get("OSTIUM_SEPOLIA_RPC", DEFAULT_TESTNET_RPC)
        else:
            net = NetworkConfig.mainnet()
            rpc = os.environ.get("OSTIUM_ARBITRUM_RPC", DEFAULT_MAINNET_RPC)
        self.sdk = OstiumSDK(net, key, rpc, verbose=verbose)
        self.address = self.sdk.w3.eth.account.from_key(key).address
        self._pair_ids = None   # lazy name->id from the live subgraph (testnet ids differ)

    @staticmethod
    def _sync(x):
        """The SubgraphClient methods are async coroutines -- run them to completion. No-op for
        already-resolved values, so it is safe whether the SDK method is sync or async."""
        return asyncio.run(x) if inspect.iscoroutine(x) else x

    # --- account ---------------------------------------------------------------
    def eth_balance(self):
        return self.sdk.w3.eth.get_balance(self.address) / 1e18

    def usdc_balance(self):
        return float(self.sdk.balance.get_usdc_balance(self.address))

    def has_gas(self):
        return self.eth_balance() > 0

    # --- testnet faucet --------------------------------------------------------
    def faucet_topup(self, target_usdc=1000.0):
        """Request test USDC until balance >= target. Each request mints get_token_amount() (10k).
        NEEDS GAS: request_tokens() sends an on-chain tx -- raises if the wallet has 0 Sepolia ETH."""
        if self.mode != "testnet":
            raise RuntimeError("faucet is testnet-only")
        if not self.has_gas():
            raise RuntimeError(f"wallet {self.address} has 0 Sepolia ETH -- fund gas first "
                               "(Arbitrum Sepolia faucet), then re-run")
        bal = self.usdc_balance()
        per = self.sdk.faucet.get_token_amount() / 10 ** USDC_DECIMALS
        reqs = 0
        while bal < target_usdc:
            if not self.sdk.faucet.can_request_tokens(self.address):
                raise RuntimeError(f"faucet cooldown active; have {bal} USDC, target {target_usdc}")
            self.sdk.faucet.request_tokens()    # on-chain tx, mints ~{per} USDC
            reqs += 1
            bal = self.usdc_balance()
        return {"requests": reqs, "per_request": per, "usdc_balance": bal}

    # --- pairs -----------------------------------------------------------------
    def pair_id(self, code):
        """Ostium numeric pair id for our code (e.g. EURUSD -> EUR-USD -> id), resolved from the LIVE
        subgraph so testnet ids are correct. None if the pair is not listed on this network."""
        if self._pair_ids is None:
            pairs = self._sync(self.sdk.subgraph.get_pairs())
            self._pair_ids = {}
            for p in pairs:
                name = (p.get("from", "") + "-" + p.get("to", "")) if isinstance(p, dict) else None
                pid = p.get("id") if isinstance(p, dict) else None
                if name and pid is not None:
                    self._pair_ids[name] = int(pid)
        # Trading pair name: WTI trades as CL-USD, COPPER as HG-USD (ohlc-override names), so prefer
        # the override; else the price-feed name. Try both against the subgraph map.
        code = code.upper()
        for name in (_instr.ostium_ohlc_overrides().get(code), _instr.ostium_pair_map().get(code)):
            if name and name in self._pair_ids:
                return self._pair_ids[name]
        return None

    # --- orders ----------------------------------------------------------------
    def market_open(self, code, side, collateral, leverage, at_price, sl_price=0.0, tp_price=0.0,
                    slippage_pct=2.0, order_type="MARKET"):
        """Open a position. side in {'long','short'}; order_type MARKET/LIMIT/STOP (at_price is the
        market mark for MARKET, or the trigger price for LIMIT/STOP). Returns the SDK result."""
        pid = self.pair_id(code)
        if pid is None:
            raise RuntimeError(f"{code} not listed on Ostium {self.mode}")
        # MUST be Decimal: the SDK does `slippage_pct * PRECISION_2` where PRECISION_2 = Decimal('100'),
        # so a Python float raises "float * Decimal" before any tx is sent (found via smoke 2026-06-07).
        self.sdk.ostium.set_slippage_percentage(Decimal(str(slippage_pct)))
        params = {"collateral": float(collateral), "leverage": float(leverage),
                  "asset_type": int(pid), "direction": (side == "long"),
                  "order_type": order_type, "tp": float(tp_price), "sl": float(sl_price)}
        return self.sdk.ostium.perform_trade(params, at_price=float(at_price))

    def orders(self):
        """Pending (limit/stop) orders for our wallet from the subgraph."""
        return self._sync(self.sdk.subgraph.get_orders(self.address)) or []

    def cancel(self, code, trade_index):
        """Cancel a resting limit/stop order by its pair + index."""
        return self.sdk.ostium.cancel_limit_order(self.pair_id(code), int(trade_index))

    def close(self, code, trade_index, market_price, percent=100):
        pid = self.pair_id(code)
        return self.sdk.ostium.close_trade(pid, trade_index, float(market_price), close_percentage=percent)

    def update_sl(self, code, trade_index, sl_price):
        return self.sdk.ostium.update_sl(self.pair_id(code), trade_index, float(sl_price))

    def open_trades(self):
        """Open positions for our wallet from the subgraph (source of truth for live state)."""
        return self._sync(self.sdk.subgraph.get_open_trades(self.address)) or []
