#!/usr/bin/env python3
"""
WALK-FORWARD -- gauntlet tier 3. See GAUNTLET.md suggestion 3.

Separates real edge from curve-fit. Single-holdout: split each pair's history IS_FRACTION in-sample
/ rest out-of-sample, judge a pair "picked" if it looked good IN-SAMPLE, then check whether those
IS-picked pairs still had an edge OUT-OF-SAMPLE. A strategy whose IS picks collapse OOS was overfit.

Per GAUNTLET.md: re-scope each strategy to its OOS SURVIVORS; a strategy with ZERO OOS survivors is
DROPPED (curve-fit, not edge). The per-(strategy,cadence) verdict here is ROBUST/OVERFIT; the
DROP-on-zero-survivors decision is applied in build_registry.py's final verdict.

This module owns the WFO DECISION (the IS pick + OOS survive rules + verdict). The IS/OOS engine
runs happen in build_registry.py (engine.run takes start/end windows), which feeds per-pair IS/OOS
stats to wfo_pair / wfo_verdict. Venue-agnostic (overfit detection) -- inherits Ostium costs from
the engine's default GATE cost.

ROLLING WFO (added 2026-06-06, GAUNTLET.md suggestion 3): a multi-fold rolling/anchored walk-forward
SUPPLEMENTS the single 70/30 holdout. It slides an in-sample window across a pair's history; after
each IS window it checks whether the IS-good edge persists on the NEXT unseen OOS window, then
stitches every fold's OOS together. An edge profitable across many regime windows is robust; one
that only worked in the single holdout but dies fold-to-fold was overfit. PER-PAIR here (each pair
sliced on its own time grid) -- consistent with FOREX's per-pair independent confirmation and
correct for a universe of heterogeneous instruments with very different histories (EUR/USD 2004,
gold 2009, natgas 2012). Purge/embargo = max-holding (time stop) + one HTF candle between IS-end and
OOS-start so a straddling trade / HTF candle cannot leak IS info into OOS.

FX windows are COARSER than sister-lab's (FX history is 15-25yr vs crypto ~5yr, so sister-lab's 90d step
would make ~70 folds): OOS tiles contiguously at `step_days` for clean regime coverage at ~15-18
folds. The decision helpers (fold boundaries, stitch, verdict) are pure functions here; the engine
IS/OOS runs happen in build_registry (which has the engine), exactly like the single-holdout split.

Run `python3 walk_forward.py` to print the WFO columns from the latest registry (read-only).
"""
from __future__ import annotations

import json
import sys

import numpy as np

from paths import REGISTRY

IS_FRACTION = 0.70   # in-sample share of each pair's bar window; the remainder is out-of-sample.

# IS "looked good" thresholds + OOS "held" thresholds. IS uses a lower trade floor than the gate
# (the IS window is ~70% of history) so a real edge is not disqualified by sample size alone.
IS_MIN_TRADES = 20
IS_MIN_PF = 1.2
OOS_MIN_PF = 1.0


def wfo_pair(is_stats: dict, oos_stats: dict) -> tuple[bool, bool]:
    """(picked, survived) for one pair from its IS and OOS metric blocks.
    picked   = IS PF>=1.2, IS net>0, IS trades>=20 (the in-sample edge that would have been chosen).
    survived = picked AND OOS PF>1.0 AND OOS net>0 (the edge persisted on unseen data)."""
    picked = ((is_stats.get("trades") or 0) >= IS_MIN_TRADES
              and (is_stats.get("profit_factor") or 0) >= IS_MIN_PF
              and (is_stats.get("net_usd") or 0) > 0)
    if not picked:
        return (False, False)
    survived = (oos_stats.get("profit_factor") or 0) > OOS_MIN_PF and (oos_stats.get("net_usd") or 0) > 0
    return (True, survived)


def wfo_verdict(picks: list, survivors: list) -> dict:
    """Registry walk_forward block from the picked/survivor pair lists.
    ROBUST when at least half the IS picks survive OOS; OVERFIT when picks exist but mostly die;
    'no IS picks' when nothing qualified in-sample (insufficient evidence, not a pass)."""
    if not picks:
        verdict = "no IS picks"
    elif len(survivors) >= max(1, len(picks) * 0.5):
        verdict = "ROBUST"
    else:
        verdict = "OVERFIT"
    return {
        "is_picked": picks,
        "oos_survived": survivors,
        "survival": f"{len(survivors)}/{len(picks)}" if picks else "0/0",
        "verdict": verdict,
    }


# ----------------------------------------------------------------------------------------------
# Rolling / anchored multi-fold WFO (per pair). Pure decision helpers; engine runs in build_registry.
# ----------------------------------------------------------------------------------------------

_DAY_MS = 86_400_000
_BANKROLL = 1000.0

# FX-appropriate windows (coarser than sister-lab -- FX history is far longer). OOS tiles at step_days.
ROLLING_WINDOWS = {
    "swing": {"is_days": 1095, "oos_days": 365, "step_days": 365},   # 3y IS, 1y OOS, yearly step
    "day":   {"is_days": 365,  "oos_days": 180, "step_days": 180},   # 1y IS, 6mo OOS, 6mo step
}
ROLLING_MIN_FOLDS = 5          # fewer usable OOS folds -> insufficient_history (not a pass)
ROLLING_IS_MIN_TRADES = 10     # per-pair trades needed in-sample to be selectable that fold
ROLLING_IS_MIN_PF = 1.2
ROLLING_STITCHED_PF = 1.05     # stitched-OOS PF for "robust"
ROLLING_FOLD_RATIO = 0.5       # fraction of OOS folds that must be profitable for "robust"


def rolling_folds(g0, g1, cad, embargo_ms, method="rolling"):
    """Fold boundaries (is0, is1, oos0, oos1) in epoch-ms over [g0, g1] for one pair.
    rolling = fixed-length IS slid by step; anchored = IS anchored at g0 and expands. Empty list
    when the cadence has no rolling window or the history is too short for one fold."""
    p = ROLLING_WINDOWS.get(cad)
    if p is None:
        return []
    is_ms, oos_ms, step = p["is_days"] * _DAY_MS, p["oos_days"] * _DAY_MS, p["step_days"] * _DAY_MS
    out, k = [], 0
    while True:
        is0 = g0 if method == "anchored" else g0 + k * step
        is1 = g0 + is_ms + k * step
        oos0 = is1 + embargo_ms
        oos1 = oos0 + oos_ms
        if oos1 > g1:
            break
        out.append((is0, is1, oos0, oos1))
        k += 1
    return out


def rolling_stitch(trades):
    """trades = [(exit_time_sec, net)] pooled across folds -> {trades, profit_factor, net_usd,
    max_dd_pct} off a $1000 equity curve ordered by exit time."""
    if not trades:
        return {"trades": 0, "profit_factor": None, "net_usd": 0.0, "max_dd_pct": 0.0}
    nets = np.array([n for _, n in sorted(trades, key=lambda x: x[0])], dtype=float)
    eq = _BANKROLL + np.cumsum(nets)
    peak = np.maximum.accumulate(eq)
    dd = (eq - peak) / peak
    w, l = nets[nets > 0], nets[nets < 0]
    pf = round(float(w.sum() / -l.sum()), 3) if l.sum() < 0 else None
    return {"trades": int(len(nets)), "profit_factor": pf, "net_usd": round(float(nets.sum()), 2),
            "max_dd_pct": round(float(dd.min()) * 100, 1)}


def rolling_verdict(fold_recs, stitched):
    """Per-pair rolling verdict from the fold records + stitched OOS.
    robust = stitched PF>=1.05 AND >=50% of OOS folds profitable; promising = stitched PF>=1.0;
    overfit = stitched PF<1.0; insufficient_history = too few usable folds."""
    considered = [f for f in fold_recs if f["oos_trades"] > 0]
    prof = [f for f in considered if f["oos_net_usd"] > 0]
    ratio = round(len(prof) / len(considered), 2) if considered else 0.0
    spf = stitched["profit_factor"] or 0
    if len(fold_recs) < ROLLING_MIN_FOLDS or not considered:
        verdict = "insufficient_history"
    elif spf >= ROLLING_STITCHED_PF and ratio >= ROLLING_FOLD_RATIO:
        verdict = "robust"
    elif spf >= 1.0:
        verdict = "promising"
    else:
        verdict = "overfit"
    return {"stitched_oos": stitched, "total_folds": len(fold_recs), "considered_folds": len(considered),
            "profitable_folds": len(prof), "profitable_fold_ratio": ratio, "verdict": verdict}


def rolling_combo_verdict(per_pair_rolling):
    """Combo-level (strategy,cadence) rolling verdict from the per-pair rolling blocks.
    Ignores pairs with insufficient history. 'overfit' if a majority of judged pairs are overfit;
    'robust' if >=50% are robust/promising; else 'promising'; 'insufficient_history' if none judged."""
    verds = [b["verdict"] for b in per_pair_rolling.values() if b.get("verdict") != "insufficient_history"]
    if not verds:
        return "insufficient_history"
    good = sum(1 for v in verds if v in ("robust", "promising"))
    overfit = sum(1 for v in verds if v == "overfit")
    if overfit > len(verds) / 2:
        return "overfit"
    if good >= max(1, len(verds) * 0.5):
        return "robust"
    return "promising"


def main():
    if not REGISTRY.exists():
        print(f"no registry at {REGISTRY}\nrun: python3 build_registry.py")
        return
    data = json.loads(REGISTRY.read_text())
    print(f"WALK-FORWARD (single-holdout IS {int(IS_FRACTION*100)}%/OOS {100-int(IS_FRACTION*100)}% "
          f"+ rolling multi-fold)\n")
    for sid, s in data.get("strategies", {}).items():
        for cad, r in (s.get("results") or {}).items():
            wf = r.get("walk_forward") or {}
            roll = r.get("rolling_wfo") or {}
            rv = roll.get("verdict", "-") if roll else "-"
            print(f"  {sid:8}{cad:7} holdout {wf.get('survival', '-'):>6} {wf.get('verdict', '-'):11} "
                  f"| rolling {rv}")


if __name__ == "__main__":
    import os
    main()
    sys.stdout.flush()
    os._exit(0)
