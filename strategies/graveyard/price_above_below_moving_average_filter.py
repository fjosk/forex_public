#!/usr/bin/env python3
"""price_above_below_moving_average_filter -- Close crosses above/below SMA20 as trend-direction entry. buku_panduan."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "price_above_below_moving_average_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, sma20",
    "long": "Close crosses from below to above SMA20",
    "short": "Close crosses from above to below SMA20",
    "desc": "Price above/below MA filter: enter on crossover of the MA (state becomes entry trigger)",
    "source": "book:buku_panduan Sec 10.5 p.57",
}


def signal(ind, pos, htf=None):
    """Long when close crosses above SMA20; short when crosses below."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    sma = ind["sma20"][pos]
    sma1 = ind["sma20"][pos - 1]
    if nan(c, c1, sma, sma1):
        return None
    if _xup(c, c1, sma, sma1):
        return "long"
    if _xdn(c, c1, sma, sma1):
        return "short"
    return None
