#!/usr/bin/env python3
"""london_ny_overlap_trend -- trade EMA momentum only in the London/NY overlap window. Session class."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "london_ny_overlap_trend",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, ema9, ema21, adx, close",
    "long": "12:00-16:00 UTC overlap, close>ema9>ema21 with ADX>20",
    "short": "12:00-16:00 UTC overlap, close<ema9<ema21 with ADX>20",
    "desc": "London/NY overlap momentum (the highest-liquidity window)",
    "source": "session-class:LDN/NY overlap",
}


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (12 <= h <= 16):
        return None
    c, e9, e21, adx = ind["close"][pos], ind["ema9"][pos], ind["ema21"][pos], ind["adx"][pos]
    if nan(c, e9, e21, adx) or adx < 20:
        return None
    if c > e9 > e21:
        return "long"
    if c < e9 < e21:
        return "short"
    return None
