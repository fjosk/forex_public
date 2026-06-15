#!/usr/bin/env python3
"""two_day_lagged_price_continuation -- Trout two-day lagged price continuation: direction of bar two days ago predicts today. New Market Wizards.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "two_day_lagged_price_continuation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Close[pos-2] > Close[pos-3] -- bar two ago closed up",
    "short": "Close[pos-2] < Close[pos-3] -- bar two ago closed down",
    "desc": "Trout lagged serial dependence: position in direction of price movement two bars prior",
    "source": "The New Market Wizards, Monroe Trout chapter, two-day lagged direction rule",
}


def signal(ind, pos, htf=None):
    """Two-day lagged price continuation."""
    if pos < 3:
        return None
    c2 = ind["close"][pos - 2]
    c3 = ind["close"][pos - 3]
    if nan(c2, c3):
        return None
    if c2 > c3:
        return "long"
    if c2 < c3:
        return "short"
    return None
