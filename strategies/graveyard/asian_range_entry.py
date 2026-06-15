#!/usr/bin/env python3
"""asian_range_entry -- ICT Asian range sweep + reversal entry. ICT official tutorial.

During the London killzone (hour_utc 7-9), detect a sweep of the Asian session range
(00:00-04:59 UTC high/low), then enter on close back inside the range.
Asian range is computed by scanning back through recent bars tagged as hour_utc < 5.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "asian_range_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m, 1h",
    "indicators": "hour_utc, high, low, close, atr",
    "long": "London KZ: price sweeps below Asian range low then closes back inside",
    "short": "London KZ: price sweeps above Asian range high then closes back inside",
    "desc": "ICT Asian range sweep and reversal during London killzone",
    "source": "web:https://innercircletrader.net/tutorials/ict-asian-range/",
}

_LOOKBACK = 60        # max bars to scan for Asian session range
_ASIAN_END_UTC = 5    # Asian session ends before hour 5 UTC
_LONDON_START = 7
_LONDON_END = 9


def signal(ind, pos, htf=None):
    """ICT Asian range sweep + reversal."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    l = ind["low"][pos]
    h = ind["high"][pos]
    if nan(hour, c, l, h):
        return None

    # Only act during London killzone
    if not (_LONDON_START <= hour <= _LONDON_END):
        return None

    # Scan back to build Asian session range (hour_utc < 5)
    asian_hi = None
    asian_lo = None
    start = max(0, pos - _LOOKBACK)
    for i in range(pos - 1, start - 1, -1):
        hr_i = ind["hour_utc"][i]
        hi_i = ind["high"][i]
        lo_i = ind["low"][i]
        if nan(hr_i, hi_i, lo_i):
            continue
        if hr_i < _ASIAN_END_UTC:
            if asian_hi is None or hi_i > asian_hi:
                asian_hi = hi_i
            if asian_lo is None or lo_i < asian_lo:
                asian_lo = lo_i
        # Stop scanning once we get past the Asian session into prior day
        elif hr_i >= _LONDON_END and asian_hi is not None:
            break

    if asian_hi is None or asian_lo is None:
        return None

    # Sweep + close-back-inside (long): low swept below range, close recovered above range lo
    if l < asian_lo and c > asian_lo:
        return "long"
    # Sweep + close-back-inside (short): high swept above range, close recovered below range hi
    if h > asian_hi and c < asian_hi:
        return "short"
    return None
