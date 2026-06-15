#!/usr/bin/env python3
"""
PnL view for the Forex Trade dashboard -- a compact, glanceable summary of the TWO trading modes
(Paper + Live) for the /pnl page.

Read-only: it reads the trader's state JSON files; it does NOT import any TRADE code (a TRADE bug
can't reach the dashboard), mirroring how registry_view reads the backtest registry. Until the
Ostium trader is built and has run, the state files don't exist, so each mode reports
started=False and the page shows a clean empty state.

Expected state file (FOREX/TRADE/state/<mode>_state.json) -- all fields read defensively, so any
reasonable shape works once the trader writes it:
  starting_balance  float   bankroll anchor (for return %)
  equity            float   current account value (realized + open unrealized)
  realized_pnl      float   sum of closed-trade net PnL (optional; falls back to sum of closed nets)
  unrealized_pnl    float   open-position mark-to-market (optional; falls back to sum of open unrealized)
  fees_paid         float   cumulative fees (open + spread + rollover + oracle) (optional; falls back
                            to summing per-trade fee fields)
  open_positions    list    [{..., "unrealized": float, "fees": float}]
  closed_trades     list    [{..., "net": float, "fees": float}]
"""
from __future__ import annotations

import json
from pathlib import Path

# plainchart/ -> LAB -> FOREX root -> TRADE/state
STATE_DIR = Path(__file__).resolve().parents[2] / "TRADE" / "state"
MODES = ("paper", "live")


def _mode_summary(mode: str) -> dict:
    f = STATE_DIR / f"{mode}_state.json"
    if not f.exists():
        return {"mode": mode, "started": False}
    try:
        s = json.loads(f.read_text())
    except (json.JSONDecodeError, OSError):
        return {"mode": mode, "started": False, "error": "state unreadable"}

    starting = s.get("starting_balance")
    equity = s.get("equity")
    closed = s.get("closed_trades") or []
    openp = s.get("open_positions") or []
    nets = [float(t.get("net", 0.0)) for t in closed]
    wins = [n for n in nets if n > 0]
    gross_w = sum(wins)
    gross_l = -sum(n for n in nets if n < 0)

    if equity is not None and starting:
        net_usd = equity - starting
    else:
        net_usd = sum(nets) if nets else None

    # Realized: prefer the trader's own field; else sum closed-trade nets.
    realized = s.get("realized_pnl")
    if realized is None:
        realized = sum(nets) if nets else None
    # Unrealized: prefer the field; else sum open-position MTM.
    unrealized = s.get("unrealized_pnl")
    if unrealized is None:
        unrealized = sum(float(p.get("unrealized", 0.0)) for p in openp) if openp else None
    # Fees: prefer cumulative field; else sum per-trade fee fields (closed + open).
    fees = s.get("fees_paid")
    if fees is None:
        fees = sum(float(t.get("fees", 0.0)) for t in closed) + \
               sum(float(p.get("fees", 0.0)) for p in openp)
        fees = fees if (closed or openp) else None

    return {
        "mode": mode,
        "started": True,
        "equity": equity,
        "starting": starting,
        "net_usd": net_usd,
        "realized": realized,
        "unrealized": unrealized,
        "fees": fees,
        "return_pct": (net_usd / starting * 100) if (net_usd is not None and starting) else None,
        "win_pct": (100.0 * len(wins) / len(nets)) if nets else None,
        # PF = gross wins / gross losses; None when there are no losses yet (shown as "--")
        "profit_factor": (gross_w / gross_l) if gross_l > 0 else None,
        "trades": len(nets),
        "open": len(openp),
    }


def summary() -> dict:
    """{'modes': {'paper': {...}, 'live': {...}}} -- one compact stat block per mode."""
    return {"modes": {m: _mode_summary(m) for m in MODES}}
