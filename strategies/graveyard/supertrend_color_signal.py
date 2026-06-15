#!/usr/bin/env python3
"""supertrend_color_signal -- SuperTrend color flip at bar close. MQL5 CodeBase 15239 (GODZILLA)."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_color_signal",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir",
    "long": "st_dir flips from bearish to bullish (color changes to green)",
    "short": "st_dir flips from bullish to bearish (color changes to red)",
    "desc": "SuperTrend color flip EA: trade on direction change at bar close; reverse on opposite color",
    "source": "Exp_SuperTrend by GODZILLA, MQL5 CodeBase 15239 (2016); tested on EURJPY H4",
}


def signal(ind, pos, htf=None):
    """Flip from bearish st_dir to bullish = long; opposite = short."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d1 < 0 and d > 0:
        return "long"
    if d1 > 0 and d < 0:
        return "short"
    return None
