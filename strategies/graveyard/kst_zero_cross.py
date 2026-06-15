#!/usr/bin/env python3
"""kst_zero_cross -- KST signal-line cross for momentum shifts. GitHub/Nikhil-Adithyan.

KST (Know Sure Thing) crosses above/below its signal line to signal bullish/bearish momentum.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kst_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "kst, kst_sig",
    "long": "KST crosses above its signal line",
    "short": "KST crosses below its signal line",
    "desc": "KST signal-line cross for momentum shifts",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """KST signal-line crossover."""
    k = ind["kst"][pos]
    k1 = ind["kst"][pos - 1]
    s = ind["kst_sig"][pos]
    s1 = ind["kst_sig"][pos - 1]
    if nan(k, k1, s, s1):
        return None
    if _xup(k, k1, s, s1):
        return "long"
    if _xdn(k, k1, s, s1):
        return "short"
    return None
