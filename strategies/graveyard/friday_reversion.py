#!/usr/bin/env python3
"""friday_reversion -- late-Friday fade of the day's move back toward the day open. DoW class."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "friday_reversion",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "dow, hour_utc, day_open, atr, close",
    "long": "Friday afternoon, price stretched >1 ATR below the day open -> fade up",
    "short": "Friday afternoon, price stretched >1 ATR above the day open -> fade down",
    "desc": "Friday position-squaring reversion toward the day open",
    "source": "session-class:day-of-week (Friday squaring)",
}

K = 1.0


def signal(ind, pos, htf=None):
    d, h = ind["dow"][pos], ind["hour_utc"][pos]
    if nan(d, h) or int(d) != 4 or not (14 <= h <= 20):    # Friday afternoon-evening UTC
        return None
    c, do, a = ind["close"][pos], ind["day_open"][pos], ind["atr"][pos]
    if nan(c, do, a) or a <= 0:
        return None
    if c < do - K * a:
        return "long"
    if c > do + K * a:
        return "short"
    return None
