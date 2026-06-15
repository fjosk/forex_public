#!/usr/bin/env python3
"""macd_line_crossover -- MACD Signal Line Crossover. Nikhil-Adithyan/Algorithmic-Trading-with-Python.

Long when MACD crosses above signal line; short when it crosses below.
No consecutive duplicate signals (handled naturally by crossover detection).
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig",
    "long": "macd crosses above macd_sig",
    "short": "macd crosses below macd_sig",
    "desc": "MACD signal line crossover (12/26/9); long on cross up, short on cross down",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """MACD crossover above/below signal line."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, ms, ms1):
        return None
    if _xup(m, m1, ms, ms1):
        return "long"
    if _xdn(m, m1, ms, ms1):
        return "short"
    return None
