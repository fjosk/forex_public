#!/usr/bin/env python3
"""
Registry view for the FOREX chart dashboard -- serves the WHOLE backtest record.

PORTED from sister-lab/LAB/dashboard/registry_view.py and adapted to FOREX: instruments are PAIRS
(not coins) and the promotion verdict follows this project's policy (ROBUST -> forward-test,
CONSIDERATION -> pool, DROP) rather than a live trade-id. Read-only: it never runs the engine,
only reads the registry that the LAB gauntlet's build_registry produces.

The gauntlet (LAB/backtest/) will run HUNDREDS-to-THOUSANDS of catalog strategies; this page is
how all of them are inspected at once. One row per (strategy, cadence) -- the grain the registry
totals live at. Per-pair detail is served separately (pairs()) and fetched lazily on row expand
to keep the summary payload small even at thousands of rows.

EXPECTED registry shape (FOREX/LAB/backtest/strategy_registry.json), tolerant of partial fills:
  { "meta": {generated, n_strategies, official_gate, pairs:[...]},
    "strategies": { "<id>": {
        style, tf, indicators, long, short, desc, source,
        forward_test: bool,                 # auto-deployed to paper+testnet forward test
        results: { "<cadence>": {
            total: {trades, win_pct, profit_factor, net_usd, return_pct, expectancy_R},
            engines: {ours_pf, vbt_pf, btpy_pf, agreement},
            gate_passing_pairs: [...],       # (or gate_passing_coins -- both accepted)
            walk_forward: {verdict}, rolling_wfo: {verdict}, stress: {verdict},
            verdict: "ROBUST"|"CONSIDERATION"|"DROP",
            per_pair: { "<PAIR>": {trades, win_pct, profit_factor, net_usd, max_dd_pct,
                                    expectancy_R, gate_pass} }   # (or per_coin -- both accepted)
        } } } } }

Cache: parsed+flattened payload held in memory keyed by the registry file mtime (mirrors
labchart.load_df). A rebuild of the registry (new mtime) invalidates it. Absent file -> None,
which the page renders as a clean "no backtests yet" empty state.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE.parent / "backtest" / "strategy_registry.json"   # FOREX/LAB/backtest/

# mtime-keyed cache of the parsed registry and the derived summary payload.
_CACHE: dict = {}


def _load() -> dict | None:
    """Parsed registry, reloaded when the file mtime changes. None if absent/unreadable."""
    if not REGISTRY.exists():
        return None
    mtime = REGISTRY.stat().st_mtime
    cached = _CACHE.get("raw")
    if cached is not None and cached[0] == mtime:
        return cached[1]
    try:
        data = json.loads(REGISTRY.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    _CACHE["raw"] = (mtime, data)
    _CACHE.pop("summary", None)   # derived payload depends on raw; drop it so it rebuilds
    return data


def _verdict(block: dict | None, key: str = "verdict") -> str:
    """Pull a verdict string from an optional sub-block (walk_forward/rolling_wfo/stress).
    Returns '-' when that filter was not run for this (strategy, cadence)."""
    if not block:
        return "-"
    return str(block.get(key, "-"))


def _gate_pairs(r: dict) -> list:
    """Pairs that cleared the gate -- accept either FOREX (pairs) or sister-lab-style (coins) key."""
    return r.get("gate_passing_pairs") or r.get("gate_passing_coins") or []


def _per_pair(r: dict) -> dict:
    return r.get("per_pair") or r.get("per_coin") or {}


def summary() -> dict | None:
    """Meta + one flat row per (strategy, cadence). No per_pair (served by pairs()).
    Shape is render-ready: the page sorts/filters these rows client-side."""
    data = _load()
    if data is None:
        return None
    cached = _CACHE.get("summary")
    if cached is not None:
        return cached

    meta = data.get("meta", {})
    rows = []
    for sid, s in data.get("strategies", {}).items():
        forward = bool(s.get("forward_test"))
        for cadence, r in (s.get("results") or {}).items():
            total = r.get("total") or {}
            eng = r.get("engines") or {}
            gate_pairs = _gate_pairs(r)
            rows.append({
                "id": sid,
                "style": s.get("style", ""),
                "tf": s.get("tf", ""),
                "cadence": cadence,
                "trades": total.get("trades", 0),
                "win_pct": total.get("win_pct"),
                "pf": total.get("profit_factor"),
                "net_usd": total.get("net_usd"),
                "return_pct": total.get("return_pct"),
                "expectancy_R": total.get("expectancy_R"),
                "ours_pf": eng.get("ours_pf"),
                "vbt_pf": eng.get("vbt_pf"),
                "btpy_pf": eng.get("btpy_pf"),
                "agreement": eng.get("agreement", "-"),
                "gate_n": len(gate_pairs),
                "gate_pairs": gate_pairs,
                "wfo": _verdict(r.get("walk_forward")),
                "rolling_wfo": _verdict(r.get("rolling_wfo")),
                "stress": _verdict(r.get("stress")),
                "verdict": str(r.get("verdict", "-")),   # ROBUST | CONSIDERATION | DROP
                "forward": forward,                       # auto-deployed to forward test
                # carried for the row-detail panel (no extra request needed)
                "indicators": s.get("indicators", ""),
                "long": s.get("long", ""),
                "short": s.get("short", ""),
                "desc": s.get("desc", ""),
                "source": s.get("source", ""),
            })

    payload = {
        "meta": {
            "generated": meta.get("generated"),
            "n_strategies": meta.get("n_strategies", len(data.get("strategies", {}))),
            "official_gate": meta.get("official_gate"),
            "pairs": meta.get("pairs") or meta.get("coins") or [],
            "n_rows": len(rows),
        },
        "rows": rows,
    }
    _CACHE["summary"] = payload
    return payload


def pairs(sid: str, cadence: str):
    """Per-pair breakdown for one (strategy, cadence). None if unknown.
    Returns the list of pair rows the registry stored for that cell."""
    data = _load()
    if data is None:
        return None
    s = data.get("strategies", {}).get(sid)
    if s is None:
        return None
    r = (s.get("results") or {}).get(cadence)
    if r is None:
        return None
    out = []
    for pair, c in _per_pair(r).items():
        out.append({
            "pair": pair,
            "trades": c.get("trades", 0),
            "win_pct": c.get("win_pct"),
            "pf": c.get("profit_factor"),
            "net_usd": c.get("net_usd"),
            "max_dd_pct": c.get("max_dd_pct"),
            "expectancy_R": c.get("expectancy_R"),
            "gate_pass": c.get("gate_pass", False),
        })
    return {"id": sid, "cadence": cadence, "pairs": out}
