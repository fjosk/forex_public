#!/usr/bin/env python3
"""filtered_entry_range_volatility -- Range contraction + 25-bar extreme close (Kevin Davey #41). web:zeta-zetra."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "filtered_entry_range_volatility",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "high, low, close",
    "long": "prior bar range < two-bar-prior range AND close >= 25-bar highest close",
    "short": "prior bar range < two-bar-prior range AND close <= 25-bar lowest close",
    "desc": "Filtered Entry: range contraction on prior bar + 25-bar extreme close (Kevin Davey #41)",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/filtered_entry.html",
}

_PERIOD = 25


def signal(ind, pos, htf=None):
    """Range contraction filter + 25-bar extreme close breakout."""
    if pos < _PERIOD + 1:
        return None
    cl = ind["close"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    hi2 = ind["high"][pos - 2]
    lo2 = ind["low"][pos - 2]
    if nan(cl, hi1, lo1, hi2, lo2):
        return None
    prior_range = hi1 - lo1
    two_bar_range = hi2 - lo2
    if two_bar_range <= 0 or prior_range >= two_bar_range:
        return None  # no range contraction
    # 25-bar extreme close (excluding current bar)
    hi_cl = cl
    lo_cl = cl
    for i in range(1, _PERIOD + 1):
        c = ind["close"][pos - i]
        if nan(c):
            return None
        if c > hi_cl:
            hi_cl = c
        if c < lo_cl:
            lo_cl = c
    if cl >= hi_cl:
        return "long"
    if cl <= lo_cl:
        return "short"
    return None
