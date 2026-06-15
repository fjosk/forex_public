#!/usr/bin/env python3
"""tsi_zero_line_crossover -- TSI zero-line crossover for momentum direction shifts. Medium/Nikhil-Adithyan.

TSI crosses above/below zero to signal bullish/bearish momentum shift.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "tsi_zero_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "tsi",
    "long": "TSI crosses above zero from below",
    "short": "TSI crosses below zero from above",
    "desc": "TSI zero-line crossover for momentum direction",
    "source": "https://medium.com/codex/coding-the-true-strength-index-and-backtesting-a-trading-strategy-in-python-24cb24b796be",
}


def signal(ind, pos, htf=None):
    """TSI zero-line cross."""
    t = ind["tsi"][pos]
    t1 = ind["tsi"][pos - 1]
    if nan(t, t1):
        return None
    if t > 0 and t1 <= 0:
        return "long"
    if t < 0 and t1 >= 0:
        return "short"
    return None
