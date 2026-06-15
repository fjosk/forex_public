#!/usr/bin/env python3
"""
One-shot Ostium TESTNET bring-up: show wallet + balances, top up test USDC from the SDK faucet to a
target, and approve USDC for trading. Run in FOREX/.venv.

  ! /home/user/FOREX/.venv/bin/python3 /home/user/FOREX/TRADE/ostium_testnet_setup.py --target 1000

GAS: the faucet (and approve) send on-chain txs, so the wallet needs a little Arbitrum Sepolia ETH.
If it has 0, this prints exactly what to do (fund gas, then re-run). Reuses HL_TESTNET_PRIVATE_KEY
(wallet <testnet-wallet>) -- testnet only.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ostium_client import OstiumClient   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, default=1000.0, help="test-USDC balance to reach")
    args = ap.parse_args()

    c = OstiumClient(mode="testnet")
    print(f"wallet:        {c.address}")
    print(f"network:       Arbitrum Sepolia (chainId {c.sdk.w3.eth.chain_id})")
    eth = c.eth_balance(); usdc = c.usdc_balance()
    per = c.sdk.faucet.get_token_amount() / 1e6
    print(f"gas (ETH):     {eth}")
    print(f"USDC:          {usdc}")
    print(f"faucet/req:    {per} test-USDC | can_request: {c.sdk.faucet.can_request_tokens(c.address)}")

    if eth <= 0:
        print("\nBLOCKED: 0 Sepolia ETH for gas. Fund the wallet, then re-run this script.")
        print("  Send a little Arbitrum Sepolia ETH (~0.02 is plenty) to:")
        print(f"    {c.address}")
        print("  Faucets (human-gated): https://www.alchemy.com/faucets/arbitrum-sepolia ,")
        print("    https://faucet.quicknode.com/arbitrum/sepolia , Google Cloud Web3 faucet.")
        print("  (Or get Sepolia L1 ETH + bridge to Arbitrum Sepolia via bridge.arbitrum.io.)")
        return

    print(f"\nrequesting faucet up to {args.target} USDC ...")
    res = c.faucet_topup(args.target)
    print("faucet:", res)
    print(f"final balances -> ETH {c.eth_balance()} | USDC {c.usdc_balance()}")
    print("Ready. USDC is approved on the first perform_trade (SDK approves internally).")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)
