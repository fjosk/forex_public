#!/usr/bin/env python3
"""
GATE -- gauntlet tier 1. See GAUNTLET.md suggestion 1.

The hard eligibility bar. A (strategy, cadence, pair) clears the gate when, priced under
costs.GATE (Ostium realistic-worst, pessimistic-but-coherent), it meets ALL thresholds below.
Mirrors the sister-lab official gate (PF>=1.2, net>$100, maxDD<30%, trades>=30).

This module owns the gate DECISION (the threshold rule + per-(strategy,cadence) summary); the
engine sweep that produces the per-pair metrics lives in build_registry.py, which imports
pair_passes_gate / gate_passing_pairs from here. Single source for the rule so nothing can tighten
one copy and miss another (the gate_rule.py precedent in sister-lab).

The gate has TWO parts (mirrors sister-lab's strict gate): (a) the per-pair Ostium-cost thresholds
above, and (b) a robustness FLOOR -- INDEPENDENT CONFIRMATION that BOTH external engines (vectorbt
+ backtesting.py, via cross_engines.py) show pooled PF>1 on the strategy's own signals. Our engine
is the candidate, not a vote (the 2026-06 sister-lab audit rule), so it does not count toward the floor.
A (strategy,cadence) that fails the floor has NO deploy-eligible pairs even if individual pairs
clear the thresholds. Walk-forward + stress (the other two tiers) then handle overfit + robustness.

Run `python3 gate.py` to print the gate column from the latest strategy_registry.json (read-only;
it does NOT run the engine -- run build_registry.py to (re)build the registry).
"""
from __future__ import annotations

import json
import sys

from paths import REGISTRY

# Official per-pair gate thresholds. Single source -- build_registry imports these.
GATE_THRESHOLDS = {
    "min_profit_factor": 1.2,
    "min_net_usd": 100.0,
    "max_drawdown_pct": 30.0,   # max_dd_pct must be SHALLOWER than this (i.e. > -30.0)
    "min_trades": 30,
}

# A (strategy,cadence) clearing on fewer pairs than this is FLAGGED survivorship-suspect (not
# dropped). Walk-forward is the real overfit filter; a legitimate edge can be single-pair after WFO.
MIN_PASSING_PAIRS = 2


def pair_passes_gate(m: dict | None) -> bool:
    """True if one pair's metric block clears the official per-pair bar under costs.GATE.

    m carries the registry per-pair keys (profit_factor, net_usd, max_dd_pct, trades). A None/empty
    block (no trades) fails. profit_factor is None when there were no losing trades AND no way to
    divide -- treated as a fail here (a strategy with too few trades to form a PF is not gate-ready;
    the trades>=30 floor catches the real cases)."""
    if not m:
        return False
    t = GATE_THRESHOLDS
    return ((m.get("net_usd") or 0) > t["min_net_usd"]
            and (m.get("profit_factor") or 0) >= t["min_profit_factor"]
            and (m.get("max_dd_pct") or -99) > -t["max_drawdown_pct"]
            and (m.get("trades") or 0) >= t["min_trades"])


def gate_passing_pairs(per_pair: dict) -> list:
    """The pairs in a (strategy,cadence) per_pair block that clear the per-pair gate, in input
    order. The independent-confirmation floor is applied by the caller (build_registry) -- a combo
    that fails the floor reports an EMPTY deploy-eligible list regardless of these per-pair passes."""
    return [pair for pair, m in per_pair.items() if pair_passes_gate(m)]


def passes_independent_confirmation(vbt_pf, btpy_pf) -> bool:
    """The robustness floor: BOTH external engines (vectorbt + backtesting.py) confirm the edge
    (pooled PF>1). A None PF (no losers, or no trades) is NOT a confirmation. Our engine is the
    candidate and is deliberately excluded -- counting it would let a house-specific artifact clear
    the floor on a single outside confirmation (the 2026-06 sister-lab audit rule)."""
    return (vbt_pf is not None and vbt_pf > 1.0) and (btpy_pf is not None and btpy_pf > 1.0)


def _rule_str() -> str:
    t = GATE_THRESHOLDS
    return (f"PF>={t['min_profit_factor']} & net>${t['min_net_usd']:.0f} & "
            f"maxDD<{t['max_drawdown_pct']:.0f}% & trades>={t['min_trades']}")


def main():
    if not REGISTRY.exists():
        print(f"no registry at {REGISTRY}\nrun: python3 build_registry.py")
        return
    data = json.loads(REGISTRY.read_text())
    print(f"GATE (official): {_rule_str()} + independent confirmation (vbt + backtesting.py PF>1)\n")
    rows = []
    for sid, s in data.get("strategies", {}).items():
        for cad, r in (s.get("results") or {}).items():
            gp = r.get("gate_passing_pairs") or r.get("gate_passing_coins") or []
            eng = r.get("engines") or {}
            rows.append((sid, cad, gp, str(r.get("verdict", "-")), eng.get("independent_pf>1", "-")))
    for sid, cad, gp, verdict, indep in sorted(rows, key=lambda x: -len(x[2])):
        flag = "  [SINGLE-PAIR: survivorship risk -- lean on walk-forward]" if 0 < len(gp) < MIN_PASSING_PAIRS else ""
        print(f"  {sid:8}{cad:7} {len(gp):>2} pairs  indep={indep:4} {verdict:13} {gp}{flag}")


if __name__ == "__main__":
    import os
    main()
    sys.stdout.flush()
    os._exit(0)   # numpy/pyarrow can SIGABRT on interpreter teardown; output already flushed
