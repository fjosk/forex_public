#!/usr/bin/env python3
"""ny_open_momentum -- at the New York open, ride the day's move-since-open. Session class."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ny_open_momentum",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, day_open, close, ema21",
    "long": "at 13:00-15:00 UTC close above the UTC day-open AND above ema21",
    "short": "at 13:00-15:00 UTC close below the UTC day-open AND below ema21",
    "desc": "New-York-open momentum continuation of the intraday move",
    "source": "session-class:NY-open drive",
}


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (13 <= h <= 15):
        return None
    c, do, e = ind["close"][pos], ind["day_open"][pos], ind["ema21"][pos]
    if nan(c, do, e):
        return None
    if c > do and c > e:
        return "long"
    if c < do and c < e:
        return "short"
    return None
