#!/usr/bin/env python3
"""ema_crossover_seykota -- EMA Crossover Seykota 3x Rule (hasnocool/tradingview-pine-scripts).
web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/EMA%20Crossover%20Strategy.pine
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_crossover_seykota",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "ema20, ema50",
    "long": "ema20 (fast) crosses above ema50 (slow, ~2.5x ratio, approximating 3x rule)",
    "short": "ema20 crosses below ema50",
    "desc": "Seykota guideline: slow EMA >= 3x fast period; approximated with ema20/ema50 (2.5x ratio)",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/EMA%20Crossover%20Strategy.pine",
}


def signal(ind, pos, htf=None):
    """EMA20/EMA50 crossover approximating Seykota's 3x slow-to-fast rule."""
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    e20_1 = ind["ema20"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    if nan(e20, e50, e20_1, e50_1):
        return None
    if _xup(e20, e20_1, e50, e50_1):
        return "long"
    if _xdn(e20, e20_1, e50, e50_1):
        return "short"
    return None
