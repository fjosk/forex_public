#!/usr/bin/env python3
"""two_ma_crossover_hochheimer -- Hochheimer dual MA crossover: SMA10 vs SMA50 stop-and-reverse. trading_systems_and_methods_kaufman_perry_j_kaufma.

Always-in stop-and-reverse: long when SMA10 crosses above SMA50, short when it crosses below.
Mirrors the Kaufman TSM comprehensive study (Tables 21-4..21-7): fast 3-25d, slow 5-60d.
Uses SMA10/SMA50 as a representative fast/slow pair.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "two_ma_crossover_hochheimer",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma10,sma50",
    "long": "SMA10 crosses above SMA50 -> buy",
    "short": "SMA10 crosses below SMA50 -> sell",
    "desc": "Hochheimer dual MA crossover: SMA10/SMA50 always-in stop-and-reverse",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch21 Tables 21-4..21-7",
}


def signal(ind, pos, htf=None):
    """Dual MA crossover: SMA10 vs SMA50."""
    if pos < 1:
        return None
    s10  = ind["sma10"][pos];  s101 = ind["sma10"][pos - 1]
    s50  = ind["sma50"][pos];  s501 = ind["sma50"][pos - 1]
    if nan(s10, s101, s50, s501):
        return None
    if _xup(s10, s101, s50, s501):
        return "long"
    if _xdn(s10, s101, s50, s501):
        return "short"
    return None
