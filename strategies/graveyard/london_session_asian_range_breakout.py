#!/usr/bin/env python3
"""london_session_asian_range_breakout -- London open breakout of Asian session range. MQL5 LONNY EA."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_session_asian_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "at London open (hour_utc==7): close > Asian session high (00-06 UTC)",
    "short": "at London open: close < Asian session low",
    "desc": "Asian-session range (00-06 UTC) breakout at London open (07 UTC)",
    "source": "web:https://www.mql5.com/en/code/17465",
}

_ASIAN_START = 0
_ASIAN_END = 6
_TRIGGER_HOUR = 7


def signal(ind, pos, htf=None):
    """Break above/below the Asian session range at London open."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    if nan(hour, c):
        return None
    if int(hour) != _TRIGGER_HOUR:
        return None
    hi = lo = None
    for i in range(pos - 1, max(pos - 30, 0), -1):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            break
        ih = int(h_i)
        if ih < _ASIAN_START or ih > _ASIAN_END:
            break
        bar_hi = ind["high"][i]
        bar_lo = ind["low"][i]
        if nan(bar_hi, bar_lo):
            continue
        hi = bar_hi if hi is None else max(hi, bar_hi)
        lo = bar_lo if lo is None else min(lo, bar_lo)
    if hi is None or lo is None:
        return None
    if c > hi:
        return "long"
    if c < lo:
        return "short"
    return None
