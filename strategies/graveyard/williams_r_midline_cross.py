#!/usr/bin/env python3
"""williams_r_midline_cross -- Williams %R crosses -50 midline with directional momentum. armelf Financial-Algorithms.

Long when willr crosses above -50 from below AND willr rising (momentum confirmed).
Short when willr crosses below -50 from above AND willr falling.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "williams_r_midline_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "willr",
    "long": "willr crosses above -50 AND willr > willr[pos-1] (rising momentum)",
    "short": "willr crosses below -50 AND willr < willr[pos-1] (falling momentum)",
    "desc": "Williams %R midline -50 crossover with momentum confirmation",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """Williams %R -50 midline crossover with momentum."""
    wr = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(wr, wr1):
        return None
    if wr1 < -50 and wr > -50 and wr > wr1:
        return "long"
    if wr1 > -50 and wr < -50 and wr < wr1:
        return "short"
    return None
