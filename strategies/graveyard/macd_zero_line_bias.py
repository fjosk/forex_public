#!/usr/bin/env python3
"""macd_zero_line_bias -- MACD zero-line bias crossover. mql5 articles/10674.

Long when MACD crosses above zero; short when it crosses below. Macro momentum bias entry.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_zero_line_bias",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd",
    "long": "MACD crosses above zero",
    "short": "MACD crosses below zero",
    "desc": "MACD zero-line bias crossover",
    "source": "https://www.mql5.com/en/articles/10674 MACD Setup Detector Strategy 1",
}


def signal(ind, pos, htf=None):
    """MACD zero-line crossover bias."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    if nan(m, m1):
        return None
    if m > 0 and m1 <= 0:
        return "long"
    if m < 0 and m1 >= 0:
        return "short"
    return None
