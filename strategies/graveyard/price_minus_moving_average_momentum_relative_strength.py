#!/usr/bin/env python3
"""price_minus_moving_average_momentum_relative_strength -- Price above/below EMA20 zero-cross trend system. Kaufman price-trend difference.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "price_minus_moving_average_momentum_relative_strength",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "ema20, close",
    "long": "Close crosses above EMA(20) -- momentum turns positive",
    "short": "Close crosses below EMA(20) -- momentum turns negative",
    "desc": "Kaufman price-MA distance momentum: close above MA = long trend; below = short trend",
    "source": "Kaufman, Trading Systems and Methods, Ch6 Price and Trend Difference, p.128",
}


def signal(ind, pos, htf=None):
    """Price vs EMA20 zero-cross (price-minus-MA momentum)."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e = ind["ema20"][pos]
    e1 = ind["ema20"][pos - 1]
    if nan(c, c1, e, e1):
        return None
    diff = c - e
    diff1 = c1 - e1
    if _xup(diff, diff1, 0.0, 0.0):
        return "long"
    if _xdn(diff, diff1, 0.0, 0.0):
        return "short"
    return None
