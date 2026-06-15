#!/usr/bin/env python3
"""
STRESS -- gauntlet tier 2. See GAUNTLET.md suggestion 2.

Re-runs each gate survivor's SAME trade set under DEGRADED OSTIUM costs (costs.STRESS_SCENARIOS:
fee_+25%, fee_+50%, slip_2x, slip_3x, harsh) and pools PnL per scenario across all pairs. A
strategy is ROBUST if pooled profit factor >= costs.SURVIVE_PF (1.0) at the verdict scenario
(costs.VERDICT_SCENARIO = "harsh"); otherwise FRAGILE.

FRAGILE is a GRADE, not an auto-reject: a fragile-but-gate-passing strategy lands in the
CONSIDERATION pool (manual review), never the bin -- over-rejecting throws away a real
Ostium-profitable edge (GAUNTLET.md promotion policy).

Single-venue: the base is Ostium and stress DEGRADES it (the direct analog of sister-lab degrading
Hyperliquid's own costs). NOT a worst-of-all-brokers Frankenstein (dropped per the operator 2026-06-06).

This module owns the stress DECISION (pooling + verdict). The engine re-runs happen in
build_registry.py, which feeds per-scenario pooled nets to stress_verdict(). The cost scenarios
themselves live in costs.py (single source).

Run `python3 stress_test.py` to print the stress column from the latest registry (read-only).
"""
from __future__ import annotations

import json
import sys

import costs as _costs
from paths import REGISTRY


def pooled_pf(nets) -> float | None:
    """Pooled profit factor over a flat list of trade nets. None when there are no losers (no
    denominator) -- the caller treats None as 'cannot confirm survival'."""
    wins = sum(n for n in nets if n > 0)
    losses = -sum(n for n in nets if n < 0)
    if losses <= 0:
        return None
    return round(wins / losses, 3)


def stress_verdict(pooled_pf_by_scenario: dict) -> dict:
    """Build the registry stress block from {scenario_name: pooled_pf}.

    survives = pooled PF at the verdict scenario ('harsh') >= SURVIVE_PF. A None harsh PF (no
    losing trades, or no trades) is NOT a pass -- robustness must be demonstrated, not assumed."""
    vpf = pooled_pf_by_scenario.get(_costs.VERDICT_SCENARIO)
    survives = vpf is not None and vpf >= _costs.SURVIVE_PF
    return {
        "scenarios": pooled_pf_by_scenario,
        "verdict_scenario": _costs.VERDICT_SCENARIO,
        "survive_pf": _costs.SURVIVE_PF,
        "survives": survives,
        "verdict": "ROBUST" if survives else "FRAGILE",
    }


def main():
    if not REGISTRY.exists():
        print(f"no registry at {REGISTRY}\nrun: python3 build_registry.py")
        return
    data = json.loads(REGISTRY.read_text())
    print(f"STRESS (degraded Ostium; verdict = {_costs.VERDICT_SCENARIO} pooled PF >= {_costs.SURVIVE_PF})\n")
    for sid, s in data.get("strategies", {}).items():
        for cad, r in (s.get("results") or {}).items():
            st = r.get("stress") or {}
            scn = st.get("scenarios") or {}
            base = scn.get("base"); harsh = scn.get(_costs.VERDICT_SCENARIO)
            print(f"  {sid:8}{cad:7} base PF {str(base):7} -> harsh PF {str(harsh):7} {st.get('verdict', '-')}")


if __name__ == "__main__":
    import os
    main()
    sys.stdout.flush()
    os._exit(0)
