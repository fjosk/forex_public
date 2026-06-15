#!/usr/bin/env python3
"""dual_ma_crossover_classic -- Classic Dual Moving Average Crossover (Wahoo MQL5 2019).
web:https://www.mql5.com/en/code/26315
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dual_ma_crossover_classic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "daily",
    "indicators": "ema50, ema200",
    "long": "ema50 crosses above ema200 (fast crosses above slow)",
    "short": "ema50 crosses below ema200",
    "desc": "Golden/dead cross: fast EMA (50) crosses slow EMA (200) with close-on-opposite exit",
    "source": "web:https://www.mql5.com/en/code/26315",
}


def signal(ind, pos, htf=None):
    """EMA50/EMA200 crossover in both directions."""
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    e50_1 = ind["ema50"][pos - 1]
    e200_1 = ind["ema200"][pos - 1]
    if nan(e50, e200, e50_1, e200_1):
        return None
    if _xup(e50, e50_1, e200, e200_1):
        return "long"
    if _xdn(e50, e50_1, e200, e200_1):
        return "short"
    return None
