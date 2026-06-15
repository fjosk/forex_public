#!/usr/bin/env python3
"""supertrend_atr_10_3 -- SuperTrend direction flip signal (ATR 10, mult 3). Adonis2115/Backtesting.

Long when SuperTrend flips to bullish (st_dir=1), short when it flips to bearish (st_dir=-1).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_atr_10_3",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir",
    "long": "SuperTrend flips to bullish (st_dir changes from -1 to 1)",
    "short": "SuperTrend flips to bearish (st_dir changes from 1 to -1)",
    "desc": "SuperTrend ATR direction flip signal",
    "source": "https://github.com/Adonis2115/Backtesting/blob/main/indicators/supertrend.py",
}


def signal(ind, pos, htf=None):
    """SuperTrend direction flip."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 != 1:
        return "long"
    if d == -1 and d1 != -1:
        return "short"
    return None
