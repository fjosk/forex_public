#!/usr/bin/env python3
"""supertrend_fast_slow_dual -- Dual SuperTrend (fast+slow) both agree for entry. web:tradingview."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_fast_slow_dual",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "st_dir, st_dir_fast",
    "long": "both slow (st_dir=1) and fast (st_dir_fast=1) SuperTrend flip to bullish simultaneously",
    "short": "both SuperTrend directions flip to bearish at the same bar",
    "desc": "Dual SuperTrend entry: slow and fast both aligned bull/bear on first bar of agreement",
    "source": "web:https://www.tradingview.com/script/DX7itST6-Strategic-Multi-Step-Supertrend-Strategy-presentTrading/",
}


def signal(ind, pos, htf=None):
    """Dual SuperTrend alignment entry."""
    sd = ind["st_dir"][pos]
    sf = ind["st_dir_fast"][pos]
    sd1 = ind["st_dir"][pos - 1]
    sf1 = ind["st_dir_fast"][pos - 1]
    if nan(sd, sf, sd1, sf1):
        return None
    bull_now = (sd == 1 and sf == 1)
    bull_prev = (sd1 == 1 and sf1 == 1)
    bear_now = (sd == -1 and sf == -1)
    bear_prev = (sd1 == -1 and sf1 == -1)
    # Enter only on the first bar both agree (new alignment)
    if bull_now and not bull_prev:
        return "long"
    if bear_now and not bear_prev:
        return "short"
    return None
