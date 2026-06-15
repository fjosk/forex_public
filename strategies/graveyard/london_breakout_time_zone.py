#!/usr/bin/env python3
"""london_breakout_time_zone -- London open breakout above/below Tokyo session range. je-suis-tm."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_breakout_time_zone",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close, atr",
    "long": "at London open (hour_utc==8): close > Tokyo session high (00-07 UTC)",
    "short": "at London open: close < Tokyo session low",
    "desc": "London open breakout above/below the Tokyo session (00-07 UTC) range",
    "source": "web:https://github.com/je-suis-tm/quant-trading",
}

_TOKYO_START = 0
_TOKYO_END = 7
_LONDON_OPEN = 8


def signal(ind, pos, htf=None):
    """Fire only at the London open bar; range = max/min of Tokyo-session bars."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    if nan(hour, c):
        return None
    if int(hour) != _LONDON_OPEN:
        return None
    hi = lo = None
    for i in range(pos - 1, max(pos - 30, 0), -1):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            break
        ih = int(h_i)
        if ih < _TOKYO_START or ih >= _LONDON_OPEN:
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
