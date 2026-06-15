#!/usr/bin/env python3
"""
build_registry -- THE FX gauntlet orchestrator. Runs the whole pipeline and emits
strategy_registry.json, the single machine-readable record the Results page reads
(LAB/plainchart/registry_view.py defines the exact shape this must produce).

Pipeline (GAUNTLET.md): for each (cadence, pair) it prepares the engine context ONCE and reuses it
across every strategy + every gauntlet stage, then aggregates per (strategy, cadence):
  1. SWEEP/GATE  -- engine.run at costs.GATE (Ostium realistic) -> per-pair metrics + pooled total;
     a pair clears the gate via gate.pair_passes_gate.
  2. STRESS      -- engine.run at each costs.STRESS_SCENARIOS, pool nets per scenario across pairs;
     verdict via stress_test.stress_verdict (ROBUST/FRAGILE at the harsh scenario).
  3. WALK-FORWARD-- engine.run on IS (end=cut) and OOS (start=cut) windows; per-pair pick/survive
     via walk_forward.wfo_pair; verdict via walk_forward.wfo_verdict.
  +  INDEPENDENT CONFIRMATION -- re-price each strategy's own signals on vectorbt + backtesting.py
     (cross_engines.py, barebones + crude flat cost), pool across pairs; the gate requires BOTH
     external engines pooled PF>1 (gate.passes_independent_confirmation). Our engine is the
     candidate, not a vote. A combo failing the floor has NO deploy-eligible pairs.
Final promotion verdict per (strategy, cadence), per GAUNTLET.md PROMOTION POLICY:
  DROP          -- gate-fail (0 gate pairs) OR zero OOS survivors (curve-fit).
  CONSIDERATION -- clears gate + has OOS survivors but FRAGILE under stress (manual-review pool).
  ROBUST        -- clears gate + has OOS survivors + survives stress (auto forward-test candidate).
A strategy's forward_test flag is set when ANY of its cadences is ROBUST.

UNIVERSE = the 14 OSTIUM-TRADEABLE pairs (universe minus the 2 Ostium does not list, EUR/JPY +
USD/ZAR). Ostium is the deploy venue, so the gauntlet decides on what we can actually trade there;
this also makes the pooled total == sum of the per-pair record. EUR/JPY + USD/ZAR (gTrade-only
fallback pairs) are out of scope for THIS gauntlet -- a separate gTrade run is future work.

THREE ENGINES: our Ostium-cost engine is the candidate; vectorbt + backtesting.py are the
independent-confirmation floor (both pooled PF>1). The registry's `engines` block carries
ours_pf / vbt_pf / btpy_pf / agreement / independent_confirmed.

Usage:
  python3 build_registry.py                       # full: all catalog strategies x 14 pairs
  python3 build_registry.py --quick               # smoke: all strategies x 2 pairs (EURUSD, XAUUSD)
  python3 build_registry.py --strategy ICHI,QQE   # subset of strategies
  python3 build_registry.py --pairs EURUSD,GBPUSD --cadence swing
  python3 build_registry.py --procs 4 --out /tmp/reg.json

Mitigates the documented numpy/pyarrow SIGABRT-on-teardown by ending with os._exit(0) after the
atomic registry write (output is already on disk).
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time

# backtest/ on path (engine, catalog, costs, gate, ...) + FOREX root (shared.*) -- mirrors the
# sister-lab tools' bootstrap. engine's own import also adds the root, but be explicit + self-contained.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np  # noqa: E402

import engine  # noqa: E402
import costs as _costs  # noqa: E402
from catalog import CATALOG  # noqa: E402
from paths import REGISTRY  # noqa: E402
from shared import instruments as _instr  # noqa: E402

import gate as _gate  # noqa: E402
import stress_test as _stress  # noqa: E402
import walk_forward as _wf  # noqa: E402
import cross_engines as _ce  # noqa: E402   # vectorbt + backtesting.py independent confirmation

# The deploy universe: Ostium-tradeable pairs only (see module docstring).
PAIRS = [p for p in _instr.universe() if p not in _instr.ostium_not_listed()]
BANKROLL = engine.BANKROLL

# Set by main() before the worker pool forks (workers inherit it). TRIAGE = cheap gate-only pre-filter
# (one base run per strategy/pair/cadence; no stress/wfo/rolling/cross-engine) -> a survivor list.
TRIAGE = False


# --- metric helpers (produce the registry's per-pair / total key names) -----------------------

def _metrics(nets, rs):
    """Per-pair or pooled metric block from net-PnL + R-multiple lists, in registry key names."""
    n = len(nets)
    if n == 0:
        return {"trades": 0, "win_pct": None, "profit_factor": None, "net_usd": 0.0, "expectancy_R": None}
    a = np.asarray(nets, dtype=float)
    w, l = a[a > 0], a[a < 0]
    pf = round(float(w.sum() / -l.sum()), 3) if l.sum() < 0 else None
    return {"trades": n, "win_pct": round(100 * len(w) / n, 1), "profit_factor": pf,
            "net_usd": round(float(a.sum()), 2),
            "expectancy_R": round(float(np.mean(rs)), 3) if rs else None}


def _wf_block(trades):
    """Slim {trades, profit_factor, net_usd} for one IS or OOS window (walk_forward.wfo_pair input)."""
    nets = [t["net"] for t in trades]
    a = np.asarray(nets, dtype=float) if nets else np.asarray([])
    if not len(a):
        return {"trades": 0, "profit_factor": None, "net_usd": 0.0}
    w, l = a[a > 0], a[a < 0]
    pf = round(float(w.sum() / -l.sum()), 3) if l.sum() < 0 else None
    return {"trades": int(len(a)), "profit_factor": pf, "net_usd": round(float(a.sum()), 2)}


def _embargo_ms(cad, ex):
    """Purge gap between IS and OOS = max-holding (time stop) + one HTF candle, in ms."""
    htf_ms = engine.TF_MS[engine.CADENCES[cad][2]]
    return int(ex.get("time_stop_h", 48)) * 3_600_000 + htf_ms


def _rolling_one(fn, ex, ctx, cad, coin):
    """Per-pair rolling WFO: slide IS/OOS folds over this pair's trimmed history, re-select IS-only
    each fold, stitch OOS. Returns the walk_forward.rolling_verdict block (with per-pair detail)."""
    ot = ctx["I"]["open_time"]
    n = ctx["n"]
    bt_year = _instr.backtest_start_year(coin)
    eff = max(205, int(np.searchsorted(ot, engine._year_ms(bt_year), side="left"))) if bt_year else 205
    g0, g1 = int(ot[eff]), int(ot[-1])
    folds = _wf.rolling_folds(g0, g1, cad, _embargo_ms(cad, ex), "rolling")
    fold_recs, stitch = [], []
    for (is0, is1, oos0, oos1) in folds:
        i0 = max(int(np.searchsorted(ot, is0)), eff)
        i1, o0, o1 = (int(np.searchsorted(ot, t)) for t in (is1, oos0, oos1))
        if i1 - i0 < 10 or o1 - o0 < 2:
            fold_recs.append({"oos_trades": 0, "oos_net_usd": 0.0})
            continue
        r_is = engine.run(coin, fn, ex, cadence=cad, ctx=ctx, start=i0, end=i1, cost_model=_costs.GATE)
        it = len(r_is["trades"])
        inet = sum(t["net"] for t in r_is["trades"])
        ipf = r_is["stats"].get("profit_factor")
        if it >= _wf.ROLLING_IS_MIN_TRADES and (ipf or 0) >= _wf.ROLLING_IS_MIN_PF and inet > 0:
            r_oos = engine.run(coin, fn, ex, cadence=cad, ctx=ctx, start=o0, end=o1, cost_model=_costs.GATE)
            onet = sum(t["net"] for t in r_oos["trades"])
            for t in r_oos["trades"]:
                stitch.append((int(t["exit_time"]) // 1000, t["net"]))
            fold_recs.append({"oos_trades": len(r_oos["trades"]), "oos_net_usd": round(onet, 2)})
        else:
            fold_recs.append({"oos_trades": 0, "oos_net_usd": 0.0})   # not selectable this fold
    stitched = _wf.rolling_stitch(stitch)
    return _wf.rolling_verdict(fold_recs, stitched)


# --- worker: one (cadence, pair) prepared once, every strategy + stage run on it ---------------

def _work(task):
    """Returns (cadence, pair, {sid: payload}). payload holds per-scenario nets, base rs+stats, and
    IS/OOS slim blocks -- everything main() needs to aggregate. One bad strategy is isolated."""
    cad, pair, sids = task
    ctx = engine.prepare(pair, cad)
    if ctx is None:
        return (cad, pair, {})
    cut = int(_wf.IS_FRACTION * ctx["n"])
    out = {}
    for sid in sids:
        m = CATALOG[sid]
        fn, ex = m["fn"], m["exit"]
        try:
            if TRIAGE:
                # Cheap pre-filter: ONE base (costs.GATE) run only -- no stress/wfo/rolling/cross.
                r = engine.run(pair, fn, ex, cadence=cad, ctx=ctx, cost_model=_costs.GATE)
                out[sid] = {"scen_nets": {"base": [t["net"] for t in r["trades"]]},
                            "base_rs": [t["r_multiple"] for t in r["trades"]],
                            "base_stats": {"max_dd_pct": r["stats"].get("max_dd_pct"),
                                           "return_pct": r["stats"].get("return_pct")}}
                continue
            scen_nets = {}
            base_rs, base_stats = [], {}
            for name in _costs.STRESS_SCENARIOS:
                r = engine.run(pair, fn, ex, cadence=cad, ctx=ctx, cost_model=_costs.for_scenario(name))
                scen_nets[name] = [t["net"] for t in r["trades"]]
                if name == "base":
                    base_rs = [t["r_multiple"] for t in r["trades"]]
                    base_stats = {"max_dd_pct": r["stats"].get("max_dd_pct"),
                                  "return_pct": r["stats"].get("return_pct")}
            r_is = engine.run(pair, fn, ex, cadence=cad, ctx=ctx, end=cut, cost_model=_costs.GATE)
            r_oos = engine.run(pair, fn, ex, cadence=cad, ctx=ctx, start=cut, cost_model=_costs.GATE)
            # Independent confirmation: re-price OUR signals on vectorbt + backtesting.py (barebones,
            # crude flat cost). Pooled across pairs in _aggregate -> the gate robustness floor.
            cp = _ce.cross_pnls(fn, ex, ctx, cad, pair)
            rolling = _rolling_one(fn, ex, ctx, cad, pair)
            out[sid] = {"scen_nets": scen_nets, "base_rs": base_rs, "base_stats": base_stats,
                        "wfo_is": _wf_block(r_is["trades"]), "wfo_oos": _wf_block(r_oos["trades"]),
                        "vbt": cp["vbt"].tolist(), "btpy": cp["btpy"].tolist(),
                        "rolling": rolling}
        except Exception as e:                       # one bad (strategy,pair) must not kill the sweep
            out[sid] = {"error": f"{type(e).__name__}: {e}"}
    return (cad, pair, out)


# --- aggregation: per-(strategy,cadence) registry block from the per-pair payloads -------------

def _aggregate(sid, cad, per_pair_payload):
    """per_pair_payload = {pair: payload}. Build the registry results[cadence] block for one strategy."""
    per_pair = {}
    rolling_per_pair = {}
    pool_nets, pool_rs = [], []
    scen_pool = {name: [] for name in _costs.STRESS_SCENARIOS}
    vbt_pool, btpy_pool = [], []
    picks, survivors = [], []

    for pair in PAIRS:
        p = per_pair_payload.get(pair)
        if not p or "scen_nets" not in p:
            continue
        base_nets = p["scen_nets"]["base"]
        mm = _metrics(base_nets, p["base_rs"])
        mm["max_dd_pct"] = p["base_stats"].get("max_dd_pct")
        mm["return_pct"] = p["base_stats"].get("return_pct")
        # PER-PAIR independent confirmation (the FX-correct reading -- a strategy may legitimately
        # work only on one instrument, e.g. gold; pooling would hide it). Both external engines must
        # show PF>1 ON THIS PAIR. gate_pass = per-pair Ostium thresholds AND per-pair confirmation.
        pv = _ce.pf_of(p.get("vbt", []))
        pb = _ce.pf_of(p.get("btpy", []))
        mm["vbt_pf"] = pv
        mm["btpy_pf"] = pb
        mm["indep_confirmed"] = _gate.passes_independent_confirmation(pv, pb)
        mm["gate_pass"] = _gate.pair_passes_gate(mm) and mm["indep_confirmed"]
        per_pair[pair] = mm
        if p.get("rolling"):
            rolling_per_pair[pair] = p["rolling"]
        pool_nets += base_nets; pool_rs += p["base_rs"]
        for name in _costs.STRESS_SCENARIOS:
            scen_pool[name] += p["scen_nets"][name]
        vbt_pool += p.get("vbt", []); btpy_pool += p.get("btpy", [])
        picked, survived = _wf.wfo_pair(p["wfo_is"], p["wfo_oos"])
        if picked:
            picks.append(pair)
            if survived:
                survivors.append(pair)

    n_pairs = max(1, len(per_pair))
    total = _metrics(pool_nets, pool_rs)
    total["return_pct"] = round(sum(pool_nets) / (n_pairs * BANKROLL) * 100, 2) if pool_nets else 0.0

    scen_pf = {name: _stress.pooled_pf(nets) for name, nets in scen_pool.items()}
    stress = _stress.stress_verdict(scen_pf)
    walk = _wf.wfo_verdict(picks, survivors)

    # Pooled engines block (informational summary row). The DEPLOY gate uses per-pair confirmation
    # (above); these pooled PFs are the at-a-glance robustness read for the Results table.
    vbt_pf = _ce.pf_of(vbt_pool)
    btpy_pf = _ce.pf_of(btpy_pool)
    ours_pf = total.get("profit_factor")
    n3 = sum(1 for x in (ours_pf, vbt_pf, btpy_pf) if x and x > 1.0)
    n_indep = sum(1 for x in (vbt_pf, btpy_pf) if x and x > 1.0)

    # Rolling WFO (multi-fold) combo verdict; an overfit roster cannot be auto-promoted.
    rolling_combo = _wf.rolling_combo_verdict(rolling_per_pair)
    rolling_ok = rolling_combo != "overfit"

    gate_pairs = [pair for pair, m in per_pair.items() if m["gate_pass"]]
    gate_ok = len(gate_pairs) >= 1

    # Promotion verdict (GAUNTLET.md): DROP on a hard fail (no gate pair OR zero single-holdout OOS
    # survivors). ROBUST needs to clear EVERY filter (gate + single-holdout WFO + rolling WFO +
    # stress). Anything gate-passing that fails stress OR rolling is CONSIDERATION (manual-review).
    if not gate_ok or len(survivors) == 0:
        verdict = "DROP"
    elif stress["survives"] and rolling_ok:
        verdict = "ROBUST"
    else:
        verdict = "CONSIDERATION"

    return {
        "total": total,
        "engines": {"ours_pf": ours_pf, "vbt_pf": vbt_pf, "btpy_pf": btpy_pf,
                    "agreement": f"{n3}/3", "independent_pf>1": f"{n_indep}/2",
                    "confirmation": "per-pair (see per_pair[*].indep_confirmed); pooled shown here"},
        "gate_passing_pairs": gate_pairs,
        "walk_forward": walk,
        "rolling_wfo": {"verdict": rolling_combo, "method": "rolling", "per_pair": rolling_per_pair},
        "stress": stress,
        "verdict": verdict,
        "per_pair": per_pair,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", help="comma-separated catalog ids (default: all)")
    ap.add_argument("--cadence", help="restrict to one cadence")
    ap.add_argument("--pairs", help="comma-separated pair codes (default: all 14 Ostium pairs)")
    ap.add_argument("--quick", action="store_true", help="smoke run: EURUSD + XAUUSD only")
    ap.add_argument("--procs", type=int, default=min(8, mp.cpu_count()), help="worker processes")
    ap.add_argument("--out", default=str(REGISTRY), help="registry output path")
    ap.add_argument("--active-only", action="store_true",
                    help="skip graveyard (dropped) strategies for a faster sweep")
    ap.add_argument("--promote", action="store_true",
                    help="after writing the registry, run strategies/promote.py (route + wire)")
    ap.add_argument("--triage", action="store_true",
                    help="CHEAP pre-filter: gate-only (one base run each, no stress/wfo/rolling/cross); "
                         "writes triage.json with the (strategy,cadence) that clear the gate on >=1 pair")
    args = ap.parse_args()

    global TRIAGE
    TRIAGE = args.triage

    sids = [s.strip() for s in args.strategy.split(",")] if args.strategy else list(CATALOG)
    sids = [s for s in sids if s in CATALOG]
    if args.active_only or args.triage:    # triage screens the ACTIVE pool, not the graveyard
        sids = [s for s in sids if CATALOG[s].get("lifecycle") != "graveyard"]
    pairs = ([p.strip().upper() for p in args.pairs.split(",")] if args.pairs
             else (["EURUSD", "XAUUSD"] if args.quick else list(PAIRS)))
    pairs = [p for p in pairs if p in PAIRS]
    cadences = sorted({c for s in sids for c in CATALOG[s]["cadences"]
                       if (not args.cadence or c == args.cadence)})

    # Tasks = (cadence, pair, strategies-at-this-cadence). Each prepares one shared ctx.
    tasks = []
    for cad in cadences:
        cad_sids = [s for s in sids if cad in CATALOG[s]["cadences"]]
        if not cad_sids:
            continue
        for pair in pairs:
            tasks.append((cad, pair, cad_sids))

    print(f"build_registry: {len(sids)} strategies x {len(pairs)} pairs x {len(cadences)} cadences "
          f"= {len(tasks)} (cadence,pair) tasks on {args.procs} procs")
    t0 = time.time()

    # raw[(cad)][pair] = {sid: payload}
    raw: dict = {cad: {} for cad in cadences}
    done = 0
    if args.procs > 1 and len(tasks) > 1:
        with mp.Pool(processes=args.procs, maxtasksperchild=8) as pool:
            for cad, pair, payload in pool.imap_unordered(_work, tasks, chunksize=1):
                raw[cad][pair] = payload
                done += 1
                print(f"  {done}/{len(tasks)}  {cad}/{pair}  ({time.time()-t0:.0f}s)")
    else:
        for task in tasks:
            cad, pair, payload = _work(task)
            raw[cad][pair] = payload
            done += 1
            print(f"  {done}/{len(tasks)}  {cad}/{pair}  ({time.time()-t0:.0f}s)")

    # TRIAGE: cheap gate-only pre-filter. A (strategy,cadence) survives if it clears the per-pair
    # gate thresholds on >=1 pair (threshold ONLY -- no independent confirmation / wfo / stress; those
    # are the strict full-gauntlet filters the survivors face next). Over-inclusive by design.
    if TRIAGE:
        survivors, screened = [], 0
        for sid in sids:
            for cad in CATALOG[sid]["cadences"]:
                if cad not in raw:
                    continue
                screened += 1
                pp, pool = {}, []
                for pair in pairs:
                    p = raw[cad].get(pair, {}).get(sid, {})
                    if not p or "scen_nets" not in p:
                        continue
                    mm = _metrics(p["scen_nets"]["base"], p["base_rs"])
                    mm["max_dd_pct"] = p["base_stats"].get("max_dd_pct")
                    if _gate.pair_passes_gate(mm):
                        pp[pair] = round(mm["profit_factor"], 3)
                    pool += p["scen_nets"]["base"]
                if pp:
                    tot = _metrics(pool, [])
                    survivors.append({"id": sid, "cadence": cad, "style": CATALOG[sid].get("style", ""),
                                      "gate_pairs": pp, "pooled_pf": tot["profit_factor"],
                                      "pooled_net": tot["net_usd"]})
        survivors.sort(key=lambda s: (-len(s["gate_pairs"]), -(s["pooled_net"] or 0)))
        triage_path = os.path.join(os.path.dirname(args.out), "triage.json")
        tmp = triage_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"generated": int(time.time()), "gate": _gate._rule_str(),
                       "note": "gate-only pre-filter (no independent-confirm/wfo/stress); survivors "
                               "advance to the full gauntlet. Over-inclusive by design.",
                       "n_screened_cells": screened, "n_survivor_cells": len(survivors),
                       "pairs": pairs, "survivors": survivors}, f, indent=1)
        os.replace(tmp, triage_path)
        n_strats = len({s["id"] for s in survivors})
        print(f"\nTRIAGE done ({time.time()-t0:.0f}s): {len(survivors)}/{screened} (strategy,cadence) "
              f"cells clear the gate on >=1 pair | {n_strats} distinct strategies survive")
        print(f"wrote {triage_path}")
        for s in survivors[:25]:
            print(f"  {s['id'][:46]:47}{s['cadence']:6} {len(s['gate_pairs'])} pairs  "
                  f"pf={s['pooled_pf']} net={s['pooled_net']}  {list(s['gate_pairs'])}")
        if len(survivors) > 25:
            print(f"  ... +{len(survivors)-25} more (see triage.json)")
        return

    # Aggregate into the registry shape.
    strategies = {}
    for sid in sids:
        m = CATALOG[sid]
        results = {}
        for cad in CATALOG[sid]["cadences"]:
            if cad not in raw:
                continue
            per_pair_payload = {pair: raw[cad].get(pair, {}).get(sid, {}) for pair in pairs}
            results[cad] = _aggregate(sid, cad, per_pair_payload)
        forward = any(r["verdict"] == "ROBUST" for r in results.values())
        strategies[sid] = {k: m.get(k, "") for k in ("style", "tf", "indicators", "long", "short",
                                                      "desc", "source")}
        strategies[sid]["forward_test"] = forward
        strategies[sid]["results"] = results

    registry = {
        "meta": {
            "generated": int(time.time()),
            "n_strategies": len(strategies),
            "official_gate": _gate._rule_str(),
            "pairs": pairs,
            "cadences": cadences,
            "universe_note": "Ostium-tradeable pairs only (EUR/JPY + USD/ZAR excluded -- gTrade-only)",
            "engine": "3-engine: our Ostium-cost engine (candidate) + vectorbt + backtesting.py "
                      "(independent confirmation floor, both pooled PF>1)",
        },
        "strategies": strategies,
    }

    out = args.out
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(registry, f, indent=1)
    os.replace(tmp, out)   # atomic: a crash mid-write never corrupts the live registry

    n_robust = sum(1 for s in strategies.values() for r in s["results"].values() if r["verdict"] == "ROBUST")
    n_cons = sum(1 for s in strategies.values() for r in s["results"].values() if r["verdict"] == "CONSIDERATION")
    n_drop = sum(1 for s in strategies.values() for r in s["results"].values() if r["verdict"] == "DROP")
    print(f"\nwrote {out}  ({time.time()-t0:.0f}s total)")
    print(f"verdicts: {n_robust} ROBUST | {n_cons} CONSIDERATION | {n_drop} DROP  "
          f"(across all strategy x cadence cells)")

    if args.promote:
        import subprocess
        promote = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "strategies", "promote.py")
        print("\n--promote: routing modules + wiring roster ...")
        subprocess.run([sys.executable, promote], check=False)


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)   # numpy/pyarrow can SIGABRT on teardown; the registry is already on disk
