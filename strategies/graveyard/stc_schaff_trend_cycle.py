#!/usr/bin/env python3
"""stc_schaff_trend_cycle -- Schaff Trend Cycle 25/75 threshold crossover. Stock Indicators for Python.

STC crosses above 25 (bullish) or drops below 75 (bearish) for doubly-smoothed trend signals.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "stc_schaff_trend_cycle",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "stc",
    "long": "STC crosses above 25 from below (bullish cycle confirmation)",
    "short": "STC crosses below 75 from above (bearish cycle confirmation)",
    "desc": "Schaff Trend Cycle 25/75 band crossover",
    "source": "https://python.stockindicators.dev/indicators/Stc/",
}


def signal(ind, pos, htf=None):
    """STC 25/75 threshold crossover."""
    s = ind["stc"][pos]
    s1 = ind["stc"][pos - 1]
    if nan(s, s1):
        return None
    if s > 25 and s1 <= 25:
        return "long"
    if s < 75 and s1 >= 75:
        return "short"
    return None
