#!/usr/bin/env python3
"""chandelier_exit_trailing_stop -- Chandelier Exit directional flip as primary entry. StockCharts/QuantifiedStrategies.

Pure Chandelier Exit system: chand_dir flip is the entry signal (no secondary filter).
The engine's ATR trailing exit handles position management.
Paired with a Donchian breakout or MA cross as trigger; here the CE flip itself is the trigger.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "chandelier_exit_trailing_stop",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "chand_dir, atr",
    "long": "chand_dir flips from -1 to +1 (CE goes bullish)",
    "short": "chand_dir flips from +1 to -1 (CE goes bearish)",
    "desc": "Chandelier Exit ATR trailing stop system -- CE flip as standalone entry",
    "source": "web:https://chartschool.stockcharts.com chandelier-exit; Charles Le Beau",
}


def signal(ind, pos, htf=None):
    """Pure Chandelier Exit flip entry."""
    cd = ind["chand_dir"][pos]
    cd1 = ind["chand_dir"][pos - 1]
    if nan(cd, cd1):
        return None
    if cd == 1 and cd1 == -1:
        return "long"
    if cd == -1 and cd1 == 1:
        return "short"
    return None
