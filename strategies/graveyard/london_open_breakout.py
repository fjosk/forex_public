#!/usr/bin/env python3
"""london_open_breakout -- break of the prior-day range at the London open hour. Session class."""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "london_open_breakout",
    "cadences": ["day"],              # 1h bars -> hourly session gating
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, prev_dhh, prev_dll, close",
    "long": "at 07:00-09:00 UTC close crosses above prior-day high",
    "short": "at 07:00-09:00 UTC close crosses below prior-day low",
    "desc": "London-open breakout of the prior UTC-day range",
    "source": "session-class:london-open ORB (forexfactory/babypips folklore)",
}


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (7 <= h <= 9):
        return None
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    hh, ll = ind["prev_dhh"][pos], ind["prev_dll"][pos]
    if nan(c, c1, hh, ll):
        return None
    if _xup(c, c1, hh, hh):
        return "long"
    if _xdn(c, c1, ll, ll):
        return "short"
    return None
