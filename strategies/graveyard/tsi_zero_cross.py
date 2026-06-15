#!/usr/bin/env python3
"""tsi_zero_cross -- TSI crosses its signal line for momentum shifts. Nikhil-Adithyan.

TSI (True Strength Index) crosses above/below its signal EMA for momentum confirmation.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "tsi_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "tsi, tsi_sig",
    "long": "TSI crosses above its signal line",
    "short": "TSI crosses below its signal line",
    "desc": "TSI signal-line cross for momentum shifts",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python Momentum/TSI.py",
}


def signal(ind, pos, htf=None):
    """TSI vs signal line crossover."""
    t = ind["tsi"][pos]
    t1 = ind["tsi"][pos - 1]
    s = ind["tsi_sig"][pos]
    s1 = ind["tsi_sig"][pos - 1]
    if nan(t, t1, s, s1):
        return None
    if _xup(t, t1, s, s1):
        return "long"
    if _xdn(t, t1, s, s1):
        return "short"
    return None
