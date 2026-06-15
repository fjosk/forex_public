#!/usr/bin/env python3
"""intraday_dayopen_revert -- fade intraday stretch away from the UTC day open. Session class.

The volume-free analog of VWAP reversion: FX/commodity bars carry volume=0 so a true VWAP is
garbage (VOLUME-GUARD); the UTC day open is the clean intraday anchor instead.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "intraday_dayopen_revert",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, day_open, atr, close",
    "long": "active session, close >2 ATR below the UTC day open -> fade up",
    "short": "active session, close >2 ATR above the UTC day open -> fade down",
    "desc": "Intraday reversion to the UTC day-open anchor",
    "source": "session-class:day-open reversion (volume-free VWAP substitute)",
}

K = 2.0


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (7 <= h <= 18):       # London+NY active hours
        return None
    c, do, a = ind["close"][pos], ind["day_open"][pos], ind["atr"][pos]
    if nan(c, do, a) or a <= 0:
        return None
    if c < do - K * a:
        return "long"
    if c > do + K * a:
        return "short"
    return None
