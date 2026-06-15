#!/usr/bin/env python3
"""london_session_opening_range_breakout -- Tokyo-range London open breakout. je-suis-tm quant-trading."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_session_opening_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "at hour_utc==8: close > max high of Tokyo session (00-07 UTC)",
    "short": "at hour_utc==8: close < min low of Tokyo session",
    "desc": "London open breakout over the Tokyo session range (00-07 UTC)",
    "source": "web:https://github.com/je-suis-tm/quant-trading",
}

_TOKYO_END = 7
_LONDON_HOUR = 8


def signal(ind, pos, htf=None):
    """Fire at London open bar; compute Tokyo session extremes from prior bars."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    if nan(hour, c):
        return None
    if int(hour) != _LONDON_HOUR:
        return None
    hi = lo = None
    for i in range(pos - 1, max(pos - 30, 0), -1):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            break
        ih = int(h_i)
        if ih >= _LONDON_HOUR:
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
