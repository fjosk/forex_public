#!/usr/bin/env python3
"""macd_zero_line_cross_12_26_9 -- MACD line crosses above/below zero: 12-day MA above 26-day MA = bullish, below = bearish. Currency Strategy practitioner guide.

tier1 momentum, FX-native. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_zero_line_cross_12_26_9",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd",
    "long": "MACD line crosses above zero (12-MA above 26-MA)",
    "short": "MACD line crosses below zero (12-MA below 26-MA)",
    "desc": "MACD zero-line cross: 12/26-day MA relationship as trend direction signal",
    "source": "Currency Strategy, Ch.4 sec 4.3.3 MACD, pp.97-100, Fig 4.8",
}


def signal(ind, pos, htf=None):
    """MACD line zero-cross."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    if nan(m, m1):
        return None
    if _xup(m, m1, 0.0, 0.0):
        return "long"
    if _xdn(m, m1, 0.0, 0.0):
        return "short"
    return None
