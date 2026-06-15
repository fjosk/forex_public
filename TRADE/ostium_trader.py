#!/usr/bin/env python3
"""
Ostium trader -- the execution bot + PnL state writer. TWO real modes:
  testnet -- Arbitrum Sepolia, REAL orders / fake (faucet) USDC  -> the dashboard "Paper" card
  live    -- Arbitrum mainnet, REAL orders / REAL USDC           -> the dashboard "Live" card
There is NO local simulator: "paper" == the real testnet account (the operator's model). Both source equity/
positions from the real Ostium account; they differ only in network + wallet.

Reuses the backtest brain so live signals match the gauntlet:
  - shared.ostium_data : live OHLC + mark      - LAB/backtest/engine.precompute : indicators
  - strategies.loader : signals                - shared.exits : ATR stop/target math
  - TRADE/ostium_client : SDK execution        - TRADE/roster.json : enabled strategies

It writes TRADE/state/<card>_state.json (card = "paper" for testnet, "live" for mainnet) so the
/pnl page (plainchart/pnl_view.py, read-only) shows EQUITY, REALIZED, UNREALIZED and FEES per card:
  {starting_balance, equity, realized_pnl, unrealized_pnl, fees_paid, network,
   open_positions:[{pair,unrealized,...}], closed_trades:[{net,fees,...}], updated}
Equity + open unrealized come from the Ostium account (USDC balance + subgraph). Realized + fees come
from the local closed-trade log this trader appends on each close (exchange equity already nets them;
this surfaces the breakdown).

MONEY GATE: no on-chain order unless armed=True AND OSTIUM_ARMED=1 (default OFF). Run in FOREX/.venv.
Native SL/TP ride on each order (perform_trade tp/sl); chandelier-trailing + close-management is the
next layer (TODO). STATUS 2026-06-07: signal/size path + state sync verified; on-chain order UNRUN.
"""
from __future__ import annotations

import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "LAB", "backtest"))

import pandas as pd  # noqa: E402

from shared import ostium_data as _od        # noqa: E402
from shared import exits as _exits            # noqa: E402
import engine as _eng                         # noqa: E402
from strategies.loader import build_catalog   # noqa: E402

ROSTER = os.path.join(_HERE, "roster.json")
STATE_DIR = os.path.join(_HERE, "state")
CADENCE_TF = {"day": ("1h", 3_000_000), "swing": ("4h", 12_000_000), "scalp": ("15m", 800_000)}
# mode -> dashboard card/state file. testnet shows on the "Paper" card; mainnet on "Live".
MODE_CARD = {"testnet": "paper", "live": "live"}

CONFIG = {"risk_pct": 0.02, "leverage": 10.0, "slippage_pct": 2.0, "min_collateral": 5.0}
EXIT = {"sl_atr": 2.0, "tp_atr": 4.0}


def _state_path(card):
    return os.path.join(STATE_DIR, f"{card}_state.json")


def _load_state(card):
    p = _state_path(card)
    if os.path.exists(p):
        try:
            return json.loads(open(p).read())
        except (OSError, json.JSONDecodeError):
            pass
    return {"realized_pnl": 0.0, "fees_paid": 0.0, "open_positions": [], "closed_trades": []}


def _write_state(card, st):
    os.makedirs(STATE_DIR, exist_ok=True)
    st["updated"] = int(time.time())
    tmp = _state_path(card) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, _state_path(card))


def live_indicators(code, cadence):
    """Live OHLC -> the SAME engine.precompute as the backtest. (I, last_index, last_close)."""
    tf, window = CADENCE_TF[cadence]
    now = int(time.time())
    rows = _od.get_ohlc(code, tf, now - window, now)
    if not rows:
        return None, None, None
    df = pd.DataFrame(rows).sort_values("open_time").reset_index(drop=True)
    if len(df) < 250:
        return None, None, None
    df["volume"] = 0.0
    df["quote_volume"] = 0.0
    return _eng.precompute(df), len(df) - 1, float(df["close"].iloc[-1])


def _roster(mode):
    try:
        r = json.loads(open(ROSTER).read())
    except (OSError, json.JSONDecodeError):
        return []
    return r.get("live_enabled" if mode == "live" else "forward_enabled", [])


def _size(equity, entry, stop_dist):
    lev = CONFIG["leverage"]
    if stop_dist <= 0 or entry <= 0:
        return 0.0
    return max(0.0, min(equity * CONFIG["risk_pct"] * entry / (lev * stop_dist), equity * 0.95))


def _sync_ostium_state(mode, client):
    """Write the real Ostium account into the mode's dashboard card state: equity = USDC balance +
    open-position unrealized; open positions from the subgraph; realized + fees from the local closed
    log. Defensive (subgraph field shapes vary)."""
    card = MODE_CARD[mode]
    st = _load_state(card)
    st["network"] = mode
    try:
        usdc = client.usdc_balance()
    except Exception:
        usdc = None
    open_rows, unrl = [], 0.0
    for t in (client.open_trades() or []):
        if not isinstance(t, dict):
            continue
        u = float(t.get("unrealizedPnl", t.get("pnl", 0.0)) or 0.0)
        unrl += u
        open_rows.append({"pair": t.get("pair"), "unrealized": round(u, 2)})
    st["open_positions"] = open_rows
    st["unrealized_pnl"] = round(unrl, 2)
    closed = st.get("closed_trades", [])
    st["realized_pnl"] = round(sum(float(c.get("net", 0.0)) for c in closed), 2)
    st["fees_paid"] = round(sum(float(c.get("fees", 0.0)) for c in closed), 2)
    if usdc is not None:
        st["starting_balance"] = st.get("starting_balance") or usdc  # anchor return% to first seen balance
        st["equity"] = round(usdc + unrl, 2)
    _write_state(card, st)
    print(f"{mode}->{card}: equity {st.get('equity')} | unreal {st['unrealized_pnl']:+.2f} | "
          f"realized {st['realized_pnl']:+.2f} | fees {st['fees_paid']:.2f} | open {len(open_rows)}")
    return st


def tick(mode="testnet", dry_run=True, verbose=True):
    """Compute signals over the mode's roster; place orders only if armed (dry_run=False AND
    OSTIUM_ARMED=1); then sync equity/positions from the Ostium account into the dashboard card."""
    armed = (not dry_run) and os.environ.get("OSTIUM_ARMED") == "1"
    from ostium_client import OstiumClient
    client = OstiumClient(mode=mode)
    try:
        equity = client.usdc_balance() or 0.0
    except Exception:
        equity = 0.0
    cat = build_catalog()
    for rec in _roster(mode):
        sid, cad = rec["id"], rec.get("cadence", "swing")
        if sid not in cat:
            continue
        for code in (rec.get("pairs") or []):
            I, i, mark = live_indicators(code, cad)
            if I is None:
                continue
            side = cat[sid]["fn"](I, i, None)
            if side not in ("long", "short"):
                continue
            atr = float(I["atr"][i]); d = 1 if side == "long" else -1
            stop_dist = _exits.stop_distance(atr, EXIT["sl_atr"], mark, _eng.MIN_STOP_PCT)
            sl = _exits.initial_stop(mark, d, stop_dist)
            tp = _exits.initial_target(mark, d, atr, EXIT["tp_atr"]) if EXIT["tp_atr"] > 0 else 0.0
            coll = _size(equity, mark, stop_dist)
            if verbose:
                print(f"  SIGNAL {sid}/{code}/{cad}: {side} @ {mark:.5g} coll={coll:.2f} sl={sl:.5g} tp={tp:.5g}")
            if armed and coll >= CONFIG["min_collateral"]:
                try:
                    res = client.market_open(code, side, coll, CONFIG["leverage"], mark,
                                             sl_price=sl, tp_price=tp, slippage_pct=CONFIG["slippage_pct"])
                    print(f"    PLACED {code} {side} -> {res}")
                except Exception as e:
                    print(f"    OPEN FAILED {code}: {type(e).__name__}: {e}")
    return _sync_ostium_state(mode, client)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="testnet", choices=["testnet", "live"],
                    help="testnet -> Paper card; live -> Live card")
    ap.add_argument("--arm", action="store_true", help="place real orders (also needs OSTIUM_ARMED=1)")
    args = ap.parse_args()
    tick(mode=args.mode, dry_run=not args.arm)


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)
