#!/usr/bin/env python3
"""
Strategy catalog -- the registry the FX gauntlet sweeps.

Since 2026-06-06 the catalog is NOT hand-written here: it is DISCOVERED from the modular,
lifecycle-organised strategy library at FOREX/strategies/ (one self-contained module per strategy,
foldered by lifecycle state -- candidates/forward/live/graveyard). This file just re-exports that
discovered CATALOG so the rest of the lab (gate/stress/walk_forward/build_registry) keeps importing
`from catalog import CATALOG` unchanged. See strategies/README.md for the standard + the promote
pipeline (gauntlet verdict -> which folder -> forward/live wiring).

VOLUME-GUARD (authoring rule): FX/commodity bars carry volume=0, so a strategy module must read only
price/OHLC/time -- never a volume series. The discovered modules are all volume-free.
"""

import os as _os
import sys as _sys

# Put the FOREX root on sys.path so `from strategies...` resolves when a tool only has LAB/backtest
# on the path (mirrors the engine bootstrap).
_FOREX_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
if _FOREX_ROOT not in _sys.path:
    _sys.path.insert(0, _FOREX_ROOT)

from strategies.loader import build_catalog   # noqa: E402

# include_graveyard=True keeps the Results record complete + re-validates dropped strategies each
# sweep. For a faster active-only run, build_registry can pass include_graveyard=False (see its CLI).
CATALOG = build_catalog(include_graveyard=True)
