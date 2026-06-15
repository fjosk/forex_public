#!/usr/bin/env python3
"""macd_signal_line_trend_system_appel -- Appel MACD: signal line crosses above/below zero for basic system; or signal crosses MACD line for alt. Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_signal_line_trend_system_appel",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd_sig",
    "long": "Signal line crosses above zero",
    "short": "Signal line crosses below zero",
    "desc": "Appel MACD: signal line zero-cross as trend direction system",
    "source": "Kaufman, Trading Systems and Methods, Ch6 MACD, p.128-130",
}


def signal(ind, pos, htf=None):
    """Signal line zero-cross for Appel MACD trend system."""
    if pos < 1:
        return None
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(s, s1):
        return None
    if _xup(s, s1, 0.0, 0.0):
        return "long"
    if _xdn(s, s1, 0.0, 0.0):
        return "short"
    return None
