#!/usr/bin/env python3
"""
promote -- the strategy lifecycle pipeline. Reads the gauntlet verdicts from the registry and ROUTES
each strategy module into its lifecycle folder, then WIRES the survivors into the trade roster.

Routing (per strategy, taking the BEST verdict across its cadences):
    ROBUST         -> strategies/live/      + roster.live_enabled       (cleared the FULL gauntlet)
    CONSIDERATION  -> strategies/forward/   + roster.forward_enabled    (gate + WFO majority; promising)
    DROP           -> strategies/graveyard/                             (failed the gauntlet)
    not in registry-> left where it is (candidates), untouched

Wiring target: FOREX/TRADE/roster.json holds `forward_enabled` + `live_enabled` -- the lists the
Ostium trader (ostium_trader.py) reads to know which strategies to run on paper/testnet (forward)
and mainnet (live), each scoped to the pairs that actually passed (gate_passing_pairs). NOTE: the
Ostium trader is still a scaffold (see FOREX/CLAUDE.md), so this registers the wiring the trader WILL
consume; order execution lands when the trader is built. ROBUST -> live is AUTOMATIC and money-gate-
free by the operator's explicit directive (2026-06-06) -- the paper->testnet->live discipline in CLAUDE.md is
deliberately overridden for this pipeline.

Moves are within FOREX/strategies/ (reversible: move a module back to candidates/ to re-screen).
roster.json is regenerated from the post-move folder state each run.

Usage:
  python3 strategies/promote.py            # apply routing + rewrite roster (default)
  python3 strategies/promote.py --dry-run  # preview the routing table, move nothing
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FOREX_ROOT = os.path.dirname(HERE)
sys.path.insert(0, FOREX_ROOT)

from strategies import loader  # noqa: E402

REGISTRY = os.path.join(FOREX_ROOT, "LAB", "backtest", "strategy_registry.json")
ROSTER = os.path.join(FOREX_ROOT, "TRADE", "roster.json")

# Verdict -> target lifecycle folder. Verdict precedence when cadences disagree (best wins).
VERDICT_RANK = {"ROBUST": 3, "CONSIDERATION": 2, "DROP": 1}
VERDICT_FOLDER = {"ROBUST": "live", "CONSIDERATION": "forward", "DROP": "graveyard"}


def _best_verdict(results: dict):
    """The highest-ranked verdict across a strategy's cadences, and the cadences that hold it."""
    best, rank = None, 0
    for cad, r in (results or {}).items():
        v = r.get("verdict")
        if v in VERDICT_RANK and VERDICT_RANK[v] > rank:
            best, rank = v, VERDICT_RANK[v]
    if best is None:
        return None, []
    cads = [cad for cad, r in results.items() if r.get("verdict") == best]
    return best, cads


def _roster_entry(sid, results, cadences):
    """Roster record for a wired strategy: the winning cadences + the pairs each cleared."""
    out = []
    for cad in cadences:
        r = results.get(cad, {})
        out.append({"id": sid, "cadence": cad,
                    "pairs": r.get("gate_passing_pairs") or [],
                    "verdict": r.get("verdict")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="preview routing; move nothing")
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--roster", default=ROSTER)
    args = ap.parse_args()

    if not os.path.exists(args.registry):
        print(f"no registry at {args.registry}\nrun: python3 LAB/backtest/build_registry.py")
        return
    data = json.loads(open(args.registry).read())
    current = loader.lifecycle_map()                 # {id: lifecycle folder it sits in now}

    moves, forward_wire, live_wire = [], [], []
    print(f"{'id':8}{'verdict':14}{'from':12}-> {'to':10} cadences")
    for sid, s in data.get("strategies", {}).items():
        if sid not in current:
            continue                                  # registry row with no module (already removed)
        results = s.get("results") or {}
        verdict, cads = _best_verdict(results)
        if verdict is None:
            continue
        target = VERDICT_FOLDER[verdict]
        frm = current[sid]
        if target != frm:
            moves.append((sid, frm, target))
        if target == "live":
            live_wire += _roster_entry(sid, results, cads)
        elif target == "forward":
            forward_wire += _roster_entry(sid, results, cads)
        print(f"{sid:8}{verdict:14}{frm:12}-> {target:10} {cads}"
              + ("  (move)" if target != frm else ""))

    if args.dry_run:
        print(f"\n[dry-run] {len(moves)} moves, "
              f"{len(live_wire)} live wires, {len(forward_wire)} forward wires -- nothing written")
        return

    for sid, frm, target in moves:
        src = loader.module_path(sid, frm)
        dst = loader.module_path(sid, target)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)

    roster = {
        "generated": int(time.time()),
        "note": ("forward_enabled = CONSIDERATION (gate + WFO majority); live_enabled = ROBUST (full "
                 "gauntlet). Scoped to each strategy's gate_passing_pairs. Read by ostium_trader "
                 "(scaffold). ROBUST->live is automatic + money-gate-free by the operator's directive."),
        "live_enabled": live_wire,
        "forward_enabled": forward_wire,
    }
    os.makedirs(os.path.dirname(args.roster), exist_ok=True)
    tmp = args.roster + ".tmp"
    with open(tmp, "w") as f:
        json.dump(roster, f, indent=1)
    os.replace(tmp, args.roster)

    print(f"\napplied {len(moves)} moves")
    print(f"wired LIVE ({len(live_wire)}): {[e['id'] for e in live_wire]}")
    print(f"wired FORWARD ({len(forward_wire)}): {[e['id'] for e in forward_wire]}")
    print(f"wrote {args.roster}")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)
