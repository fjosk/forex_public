#!/usr/bin/env python3
"""supertrend_ema200_swing -- SuperTrend flip filtered by EMA200 side. web:forextester.com.

EMA200 as macro trend filter; SuperTrend flip as entry timing. Only longs above EMA200,
only shorts below. Trail stop along st_line. No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "supertrend_ema200_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "st_dir, st_line, ema200",
    "long": "close > ema200 AND st_dir flips from -1 to +1",
    "short": "close < ema200 AND st_dir flips from +1 to -1",
    "desc": "SuperTrend flip with EMA200 macro trend filter",
    "source": "web:https://forextester.com/blog/supertrend-indicator/",
}


def signal(ind, pos, htf=None):
    """SuperTrend flip gated by EMA200 side."""
    c = ind["close"][pos]
    ema = ind["ema200"][pos]
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(c, ema, sd, sdp):
        return None
    if c > ema and sd == 1 and sdp == -1:
        return "long"
    if c < ema and sd == -1 and sdp == 1:
        return "short"
    return None
