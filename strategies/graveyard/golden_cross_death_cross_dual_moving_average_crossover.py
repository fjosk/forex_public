#!/usr/bin/env python3
"""golden_cross_death_cross_dual_moving_average_crossover -- Golden/Death Cross: SMA50 crosses SMA200. buku_panduan."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "golden_cross_death_cross_dual_moving_average_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma50, sma200",
    "long": "SMA50 crosses above SMA200 (Golden Cross)",
    "short": "SMA50 crosses below SMA200 (Death Cross)",
    "desc": "Classic Golden/Death Cross dual MA crossover using SMA50 and SMA200",
    "source": "book:buku_panduan Sec 10.2",
}


def signal(ind, pos, htf=None):
    """Golden Cross / Death Cross on SMA50 vs SMA200."""
    if pos < 1:
        return None
    fast = ind["sma50"][pos]
    fast1 = ind["sma50"][pos - 1]
    slow = ind["sma200"][pos]
    slow1 = ind["sma200"][pos - 1]
    if nan(fast, fast1, slow, slow1):
        return None
    if _xup(fast, fast1, slow, slow1):
        return "long"
    if _xdn(fast, fast1, slow, slow1):
        return "short"
    return None
