#!/usr/bin/env python3
"""asymmetric_triple_weekday_high_low -- Monday/Friday 15-bar high/low extreme breakout. web:zeta-zetra/Davey."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "asymmetric_triple_weekday_high_low",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "dow, high, low, close",
    "long": "Monday or Friday, current high and close both at 15-bar high",
    "short": "Monday or Friday, current low and close both at 15-bar low",
    "desc": "Asymmetric Triple: weekday (Mon/Fri) 15-bar extreme high/low close breakout (Kevin Davey)",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/asymmetric_triple.html",
}

_PERIOD = 15


def signal(ind, pos, htf=None):
    """Monday or Friday: current bar high/close at 15-bar high; low/close at 15-bar low."""
    if pos < _PERIOD:
        return None
    dow = ind["dow"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    cl = ind["close"][pos]
    if nan(dow, hi, lo, cl):
        return None
    # dow: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    if dow not in (0, 4):
        return None
    roll_hi = hi
    roll_lo = lo
    roll_cl_hi = cl
    roll_cl_lo = cl
    for i in range(1, _PERIOD):
        h = ind["high"][pos - i]
        l = ind["low"][pos - i]
        c = ind["close"][pos - i]
        if nan(h, l, c):
            return None
        if h > roll_hi:
            roll_hi = h
        if l < roll_lo:
            roll_lo = l
        if c > roll_cl_hi:
            roll_cl_hi = c
        if c < roll_cl_lo:
            roll_cl_lo = c
    if hi >= roll_hi and cl >= roll_cl_hi:
        return "long"
    if lo <= roll_lo and cl <= roll_cl_lo:
        return "short"
    return None
