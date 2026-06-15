#!/usr/bin/env python3
"""commodity_channel_index_zero_cross -- CCI Zero-Line Cross. Nikhil-Adithyan/Algorithmic-Trading-with-Python.

CCI crosses above zero = long entry (bullish momentum shift).
CCI crosses below zero = short entry.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "commodity_channel_index_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "cci",
    "long": "cci crosses from negative to positive (zero-line cross up)",
    "short": "cci crosses from positive to negative (zero-line cross down)",
    "desc": "CCI zero-line crossover: momentum entry on price diverging from recent average",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """CCI zero-line cross for momentum entry."""
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    if nan(cc, cc1):
        return None
    if _xup(cc, cc1, 0.0, 0.0):
        return "long"
    if _xdn(cc, cc1, 0.0, 0.0):
        return "short"
    return None
