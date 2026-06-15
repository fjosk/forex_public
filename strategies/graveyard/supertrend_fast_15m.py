#!/usr/bin/env python3
"""supertrend_fast_15m -- Fast SuperTrend direction flip 15m scalp. ForexTester guide.

Uses st_dir_fast (tighter parameters) to detect trend flip. Enter on flip bar where
close confirms the new direction (bullish body for long, bearish body for short).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_fast_15m",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "15m",
    "indicators": "st_dir_fast, st_line, open, close",
    "long": "st_dir_fast flips from <= 0 to > 0 AND close > open (bullish body)",
    "short": "st_dir_fast flips from >= 0 to < 0 AND close < open (bearish body)",
    "desc": "Fast SuperTrend (tight params) flip entry 15m scalp",
    "source": "web:https://forextester.com/blog/supertrend-indicator/",
}


def signal(ind, pos, htf=None):
    """Fast SuperTrend direction flip 15m scalp."""
    sf0 = ind["st_dir_fast"][pos]
    sf1 = ind["st_dir_fast"][pos - 1]
    o = ind["open"][pos]
    c = ind["close"][pos]
    if nan(sf0, sf1, o, c):
        return None
    if sf0 > 0 and sf1 <= 0 and c > o:
        return "long"
    if sf0 < 0 and sf1 >= 0 and c < o:
        return "short"
    return None
