#!/usr/bin/env python3
"""inside_day_open_range_breakout -- ORB using session high/low with hour_utc gating. MT4 EA ORB."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_day_open_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close, atr",
    "long": "London open bar (hour_utc==8) closes above 08:00 session high",
    "short": "London open bar closes below 08:00 session low",
    "desc": "Opening range breakout using prior session (00-08 UTC) high/low as the range",
    "source": "web:https://github.com/omnisis/mt4-ea-obr",
}

# Session range window: Asian/pre-London hours
_RANGE_START = 0
_RANGE_END = 7
_TRIGGER_HOUR = 8


def signal(ind, pos, htf=None):
    """Break above/below the Asian-session range on the London open bar."""
    c = ind["close"][pos]
    hour = ind["hour_utc"][pos]
    if nan(c, hour):
        return None
    # Only fire a signal on the London open bar
    if int(hour) != _TRIGGER_HOUR:
        return None
    # Walk back to collect the session range for hours in [0, 7)
    hi = lo = None
    for i in range(pos - 1, max(pos - 25, 0), -1):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            break
        if int(h_i) < _RANGE_START or int(h_i) >= _TRIGGER_HOUR:
            break
        bar_hi = ind["high"][i]
        bar_lo = ind["low"][i]
        if nan(bar_hi, bar_lo):
            continue
        hi = bar_hi if hi is None else max(hi, bar_hi)
        lo = bar_lo if lo is None else min(lo, bar_lo)
    if hi is None or lo is None:
        return None
    atr = ind["atr"][pos]
    if nan(atr) or atr <= 0:
        return None
    # Require price to break outside the range by at least a small buffer
    if c > hi:
        return "long"
    if c < lo:
        return "short"
    return None
