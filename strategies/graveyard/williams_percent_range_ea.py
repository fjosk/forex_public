#!/usr/bin/env python3
"""williams_percent_range_ea -- Williams %R exits oversold/overbought zone -> trade in direction of cross.

No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_percent_range_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "willr",
    "long": "willr crosses above -80 (exits oversold zone)",
    "short": "willr crosses below -20 (exits overbought zone)",
    "desc": "Williams %R mean-reversion: trade when WPR exits oversold (<-80) or overbought (>-20) zone",
    "source": "mql4tutorial.com MQL4 Tutorial Basics-49 Simple WPR EA",
}

_OVERSOLD = -80.0
_OVERBOUGHT = -20.0


def signal(ind, pos, htf=None):
    """Williams %R crossover of oversold/overbought thresholds."""
    if pos < 1:
        return None
    w0 = ind["willr"][pos]
    w1 = ind["willr"][pos - 1]
    if nan(w0, w1):
        return None
    # Long: WPR crosses up through -80 (exits oversold)
    if w0 > _OVERSOLD and w1 <= _OVERSOLD:
        return "long"
    # Short: WPR crosses down through -20 (exits overbought)
    if w0 < _OVERBOUGHT and w1 >= _OVERBOUGHT:
        return "short"
    return None
