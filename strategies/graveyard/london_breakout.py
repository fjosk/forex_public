#!/usr/bin/env python3
"""london_breakout -- London session breakout of the Asian range. QuantifiedStrategies.

Computes the Asian session high/low (00:00-06:59 UTC) by scanning back through
recent bars. At London open (07:00-09:00 UTC), enters on breakout above Asian high
or below Asian low. Range-width filter: skip when range > 0.6 * atr * 6 (wide range).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close, atr",
    "long": "07-09 UTC: close breaks above Asian session high (00-07 UTC) and range not too wide",
    "short": "07-09 UTC: close breaks below Asian session low and range not too wide",
    "desc": "London session breakout of Asian range (00-07 UTC)",
    "source": "web:https://www.quantifiedstrategies.com/london-breakout-strategy/",
}

_ASIAN_END_UTC = 7     # Asian session ends before 07:00 UTC
_LONDON_START = 7
_LONDON_END = 9
_LOOKBACK = 48          # max bars to scan back for Asian range
_RANGE_ATR_FACTOR = 3.0 # skip if asian_range > factor * atr (too wide)


def signal(ind, pos, htf=None):
    """London breakout of Asian session range."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    atr = ind["atr"][pos]
    if nan(hour, c, c1, atr) or atr == 0:
        return None
    if not (_LONDON_START <= hour <= _LONDON_END):
        return None

    # Scan back to find Asian session bars (hour_utc < 7) from today
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
        elif asian_hi is not None:
            # Crossed back into previous session - stop scanning
            break

    if asian_hi is None or asian_lo is None:
        return None

    # Wide-range filter
    asian_range = asian_hi - asian_lo
    if asian_range > _RANGE_ATR_FACTOR * atr:
        return None

    # Breakout long: close above Asian high
    if c > asian_hi and c1 <= asian_hi:
        return "long"
    # Breakout short: close below Asian low
    if c < asian_lo and c1 >= asian_lo:
        return "short"
    return None
