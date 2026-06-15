#!/usr/bin/env python3
"""macd_oscillator_cross -- MACD line zero-line crossover. je-suis-tm/quant-trading.

Enter long when MACD crosses above zero, short when it crosses below zero.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_oscillator_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd",
    "long": "MACD line crosses above zero",
    "short": "MACD line crosses below zero",
    "desc": "MACD zero-line crossover",
    "source": "https://github.com/je-suis-tm/quant-trading MACD Oscillator backtest.py",
}


def signal(ind, pos, htf=None):
    """MACD zero-line cross."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    if nan(m, m1):
        return None
    if m > 0 and m1 <= 0:
        return "long"
    if m < 0 and m1 >= 0:
        return "short"
    return None
