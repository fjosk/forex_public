#!/usr/bin/env python3
"""
Strategy loader -- discovers the modular strategy library and builds the CATALOG the gauntlet sweeps.

The strategy library is lifecycle-organised: every strategy is ONE self-contained module
strategies/<lifecycle>/<ID>.py exposing `META` (definition) + `signal(ind, pos, htf)` (decision).
The lifecycle folder a module sits in IS its state -- promote.py moves modules between folders based
on the gauntlet verdict (see strategies/README.md):

    candidates/  authored, in the screening pool (not yet routed)
    forward/     CONSIDERATION -- cleared gate + WFO majority; wired to the forward test
    live/        ROBUST -- cleared the FULL gauntlet; wired to live
    graveyard/   DROP -- failed the gauntlet (kept for the record / revival)

This module turns those folders into the CATALOG dict the rest of the lab already expects
(LAB/backtest/catalog.py re-exports it, so gate/stress/walk_forward/build_registry are unchanged):

    CATALOG[id] = {fn, cadences, exit, asset_classes, style, tf, indicators, long, short, desc,
                   source, lifecycle}

By default build_catalog() loads the ACTIVE set (candidates + forward + live) AND graveyard, so the
Results record stays complete and dropped strategies are continuously re-validated; pass
include_graveyard=False for a faster active-only sweep. PURE-ish: imports strategy modules only.
"""
from __future__ import annotations

import importlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))

LIFECYCLES = ["candidates", "forward", "live", "graveyard"]
ACTIVE = ["candidates", "forward", "live"]   # the deploy-relevant states (graveyard is dropped)


def _iter_modules(lifecycles):
    """Yield (id, lifecycle, module) for every <ID>.py in the given lifecycle folders."""
    for lc in lifecycles:
        d = os.path.join(HERE, lc)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".py") or fn.startswith("_"):
                continue
            sid = fn[:-3]
            mod = importlib.import_module(f"strategies.{lc}.{sid}")
            yield sid, lc, mod


def build_catalog(include_graveyard: bool = True) -> dict:
    """The CATALOG dict (id -> definition) discovered from the lifecycle folders. A module missing
    META or signal, or whose META['id'] disagrees with its filename, is a hard error (fail loud --
    a malformed strategy must not silently vanish from the sweep)."""
    lifecycles = LIFECYCLES if include_graveyard else ACTIVE
    catalog: dict = {}
    for sid, lc, mod in _iter_modules(lifecycles):
        meta = getattr(mod, "META", None)
        fn = getattr(mod, "signal", None)
        if meta is None or not callable(fn):
            raise ValueError(f"strategies/{lc}/{sid}.py missing META or signal()")
        if meta.get("id") != sid:
            raise ValueError(f"strategies/{lc}/{sid}.py META id {meta.get('id')!r} != filename {sid!r}")
        if sid in catalog:
            raise ValueError(f"duplicate strategy id {sid!r} (in two lifecycle folders)")
        catalog[sid] = {
            "fn": fn,
            "cadences": meta["cadences"],
            "exit": meta["exit"],
            "asset_classes": meta.get("asset_classes", []),
            "style": meta.get("style", ""),
            "tf": meta.get("tf", ""),
            "indicators": meta.get("indicators", ""),
            "long": meta.get("long", ""),
            "short": meta.get("short", ""),
            "desc": meta.get("desc", ""),
            "source": meta.get("source", ""),
            "lifecycle": lc,
        }
    return catalog


def lifecycle_map() -> dict:
    """{id: lifecycle} across ALL folders -- used by promote.py to know where each module lives."""
    return {sid: lc for sid, lc, _ in _iter_modules(LIFECYCLES)}


def module_path(sid: str, lifecycle: str) -> str:
    """Absolute path of a strategy module file in a given lifecycle folder."""
    return os.path.join(HERE, lifecycle, f"{sid}.py")
