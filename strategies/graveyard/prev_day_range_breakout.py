#!/usr/bin/env python3
"""prev_day_range_breakout -- pure prior-UTC-day high/low breakout, any hour. Session class."""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "prev_day_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "prev_dhh, prev_dll, close",
    "long": "close crosses above the prior-day high",
    "short": "close crosses below the prior-day low",
    "desc": "Prior-day range breakout (daily structure, time-anchored)",
    "source": "session-class:prior-day range break",
}


def signal(ind, pos, htf=None):
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    hh, ll = ind["prev_dhh"][pos], ind["prev_dll"][pos]
    if nan(c, c1, hh, ll):
        return None
    if _xup(c, c1, hh, hh):
        return "long"
    if _xdn(c, c1, ll, ll):
        return "short"
    return None
