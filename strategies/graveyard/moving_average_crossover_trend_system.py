#!/usr/bin/env python3
"""moving_average_crossover_trend_system -- EMA9 crosses EMA50 for trend entry. the_new_market_wizards."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "moving_average_crossover_trend_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema9, ema50",
    "long": "EMA9 crosses above EMA50 (fast MA over slow MA)",
    "short": "EMA9 crosses below EMA50 (fast MA under slow MA)",
    "desc": "MA crossover trend system: fast EMA9 crossing slow EMA50",
    "source": "book:the_new_market_wizards Glossary Moving average / Trend-following system",
}


def signal(ind, pos, htf=None):
    """EMA9 crosses EMA50 for trend reversal entry."""
    if pos < 1:
        return None
    fast = ind["ema9"][pos]
    fast1 = ind["ema9"][pos - 1]
    slow = ind["ema50"][pos]
    slow1 = ind["ema50"][pos - 1]
    if nan(fast, fast1, slow, slow1):
        return None
    if _xup(fast, fast1, slow, slow1):
        return "long"
    if _xdn(fast, fast1, slow, slow1):
        return "short"
    return None
