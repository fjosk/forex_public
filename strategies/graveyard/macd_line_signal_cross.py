#!/usr/bin/env python3
"""macd_line_signal_cross -- MACD line crosses its signal line. MetaQuotes MT5 sample.

Classic MACD crossover: enter long on upward cross, short on downward cross.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_line_signal_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig",
    "long": "MACD line crosses above signal line",
    "short": "MACD line crosses below signal line",
    "desc": "MACD line / signal line crossover",
    "source": "https://www.mql5.com/en/code/262 MetaQuotes MACD Sample EA",
}


def signal(ind, pos, htf=None):
    """MACD line vs signal line crossover."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, s, s1):
        return None
    if _xup(m, m1, s, s1):
        return "long"
    if _xdn(m, m1, s, s1):
        return "short"
    return None
