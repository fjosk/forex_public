#!/usr/bin/env python3
"""chandelier_exit_strategy -- Chandelier Exit stop-and-reverse strategy. hasnocool / Charles Le Beau / Elder.

Enter long when chand_dir flips from -1 to +1; enter short when it flips from +1 to -1. The
engine applies the TREND_FLIP archetype (exit on opposite signal) mirroring the Pine script's
signal-reversal exit.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "chandelier_exit_strategy",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "chand_dir, atr",
    "long": "chand_dir transitions from -1 to +1 (dir == 1 and dir[1] == -1)",
    "short": "chand_dir transitions from +1 to -1 (dir == -1 and dir[1] == 1)",
    "desc": "Chandelier Exit stop-and-reverse: enter on CE direction flip, exit on opposing flip",
    "source": "https://github.com/hasnocool/tradingview-pine-scripts (Chandelier Exit - Strategy.pine)",
}


def signal(ind, pos, htf=None):
    """Chandelier direction stop-and-reverse."""
    d = ind["chand_dir"][pos]
    d1 = ind["chand_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
