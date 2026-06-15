#!/usr/bin/env python3
"""supertrend_crossover_daily -- SuperTrend flip on daily chart (multiplier 3). web:algomatictrading.substack.com.

Enter long when SuperTrend direction flips bullish (-1 to +1); enter short when it flips
bearish. Trail stop at the SuperTrend line. 2005-2026 backtest data on Nasdaq/Gold cited.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_crossover_daily",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "st_dir, st_line",
    "long": "st_dir flips from -1 to +1 (price reclaims above SuperTrend line)",
    "short": "st_dir flips from +1 to -1 (price breaks below SuperTrend line)",
    "desc": "SuperTrend crossover daily (ATR multiplier 3) with trailing stop at st_line",
    "source": "web:https://algomatictrading.substack.com/p/strategy-18-the-supertrend-crossover",
}


def signal(ind, pos, htf=None):
    """SuperTrend direction flip -- daily variant."""
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(sd, sdp):
        return None
    if sd == 1 and sdp == -1:
        return "long"
    if sd == -1 and sdp == 1:
        return "short"
    return None
