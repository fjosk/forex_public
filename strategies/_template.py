#!/usr/bin/env python3
"""<ID> -- <one-line description>. <source>.

COPY this file to strategies/candidates/<ID>.py to author a new strategy, then fill in META + the
signal logic. One self-contained module per strategy is the standard (see strategies/README.md).

RULES:
- Price/OHLC/time ONLY. NEVER read a volume series -- FX/commodity bars carry volume=0, so a
  volume-based rule produces garbage (VOLUME-GUARD).
- The signal is PURE: no I/O, no state, no globals. It returns the raw side; the engine (and the
  future Ostium trader) apply the exit envelope from META["exit"].
- META["id"] MUST equal the filename (without .py) -- the loader enforces this.
- Read indicator arrays by name from `ind` (see LAB/backtest/engine.precompute for what is available
  and exactly how each is spelled). Guard warm-up bars with nan(...).
"""
from strategies._common import nan, TREND, ALL_CLASSES   # pick the exit preset that fits (TREND/REVERT/BREAK)

META = {
    "id": "TEMPLATE",                 # MUST match the filename
    "cadences": ["swing"],            # engine cadences to test: "day" (1h) / "swing" (4h) / "scalp" (15m)
    "exit": TREND,                    # ATR exit archetype from _common, or a custom dict
    "asset_classes": ALL_CLASSES,     # documentation only (engine picks real spread per traded pair)
    "style": "trend",
    "tf": "4h",
    "indicators": "list the indicators the rule reads",
    "long": "human-readable long condition",
    "short": "human-readable short condition",
    "desc": "one-line description",
    "source": "where this idea came from",
}


def signal(ind, pos, htf=None):
    """<one-line description>."""
    # Example: read indicators, guard NaN, return 'long' / 'short' / None.
    c = ind["close"][pos]
    if nan(c):
        return None
    return None
