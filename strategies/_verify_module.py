#!/usr/bin/env python3
"""
Verify a strategy module (or all candidates) without running the full engine: import it, build a
synthetic `ind` dict carrying EVERY engine.precompute key, and call signal() at several bar indices.
Catches the common authoring faults cheaply: import errors, a bad/missing META id, and -- the big
one -- reading an indicator key that does NOT exist in precompute (KeyError). Real trade behaviour is
judged later by the gauntlet; this just proves the module is wired correctly.

Usage:
  python3 strategies/_verify_module.py <id> [<id> ...]   # verify named candidate modules
  python3 strategies/_verify_module.py --all             # verify every module the loader sees
Exit code 0 if all pass, 1 if any fail (so it is scriptable).
"""
from __future__ import annotations

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))           # FOREX root
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "LAB", "backtest"))

import numpy as np  # noqa: E402


def _synthetic_ind():
    """An `ind` dict with every precompute key as a small non-degenerate array (so comparisons and
    cross-checks at pos and pos-k exercise real branches without NaN-short-circuiting everything)."""
    import engine
    import pandas as pd
    n = 300
    base = np.linspace(1.0, 2.0, n) + np.sin(np.arange(n) / 7.0) * 0.05
    df = pd.DataFrame({"open_time": np.arange(n) * 3_600_000, "open": base,
                       "high": base * 1.01, "low": base * 0.99, "close": base,
                       "volume": np.zeros(n), "quote_volume": np.zeros(n)})
    # Synthetic higher-timeframe dict mirroring engine._htf_map (bias/slope/adx4) so signals that
    # read htf are exercised the way the engine calls them (not with None).
    htf = {"bias": np.where(np.arange(n) % 2 == 0, 1.0, -1.0),
           "slope": np.sign(np.diff(base, prepend=base[0])),
           "adx4": 15.0 + (np.arange(n) % 20)}
    return engine.precompute(df), htf, n


def verify(sid, ind, htf, n, lifecycles=("candidates", "forward", "live", "graveyard")):
    """Import strategies.<lifecycle>.<sid> and exercise signal() at a spread of indices."""
    mod = None
    for lc in lifecycles:
        if os.path.exists(os.path.join(HERE, lc, f"{sid}.py")):
            mod = importlib.import_module(f"strategies.{lc}.{sid}")
            break
    if mod is None:
        return False, "module file not found"
    meta = getattr(mod, "META", None)
    fn = getattr(mod, "signal", None)
    if meta is None or not callable(fn):
        return False, "missing META or signal()"
    if meta.get("id") != sid:
        return False, f"META id {meta.get('id')!r} != filename {sid!r}"
    for i in (250, 270, 290, n - 1):
        try:
            r = fn(ind, i, htf)
        except Exception as e:
            return False, f"signal() raised at i={i}: {type(e).__name__}: {e}"
        if r not in (None, "long", "short"):
            return False, f"signal() returned {r!r} (must be long/short/None)"
    return True, "ok"


def main():
    args = sys.argv[1:]
    ind, htf, n = _synthetic_ind()
    if args == ["--all"]:
        from strategies.loader import build_catalog
        ids = list(build_catalog())
    else:
        ids = args
    if not ids:
        print("usage: _verify_module.py <id> [...] | --all")
        return 1
    fails = []
    for sid in ids:
        ok, msg = verify(sid, ind, htf, n)
        if not ok:
            fails.append((sid, msg))
            print(f"FAIL {sid}: {msg}")
    print(f"{len(ids) - len(fails)}/{len(ids)} modules verified OK")
    return 1 if fails else 0


if __name__ == "__main__":
    rc = main()
    sys.stdout.flush()
    os._exit(rc)
