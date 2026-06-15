#!/usr/bin/env python3
"""sma200_trend_ema9_entry -- SMA200 macro filter + EMA9/EMA21 crossover entry. web:babypips.com.

Classic two-tier MA strategy: SMA200 macro direction; EMA9/EMA21 crossover timing.
Only longs above SMA200, only shorts below. No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "sma200_trend_ema9_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma200, ema9, ema21",
    "long": "close > sma200 AND ema9 crosses above ema21",
    "short": "close < sma200 AND ema9 crosses below ema21",
    "desc": "SMA200 trend filter with EMA9/EMA21 crossover entry",
    "source": "web:https://www.babypips.com/learn/forex/moving-average-crossover-trading",
}


def signal(ind, pos, htf=None):
    """EMA9/21 crossover gated by SMA200 trend side."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    e9, e9p = ind["ema9"][pos], ind["ema9"][pos - 1]
    e21, e21p = ind["ema21"][pos], ind["ema21"][pos - 1]
    if nan(c, sma, e9, e9p, e21, e21p):
        return None
    if c > sma and _xup(e9, e9p, e21, e21p):
        return "long"
    if c < sma and _xdn(e9, e9p, e21, e21p):
        return "short"
    return None
