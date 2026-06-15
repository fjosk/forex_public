#!/usr/bin/env python3
"""monday_range_breakout -- Monday break of the prior (Friday) day range. Day-of-week class."""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "monday_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "dow, prev_dhh, prev_dll, close",
    "long": "on Monday, close crosses above the prior-session high",
    "short": "on Monday, close crosses below the prior-session low",
    "desc": "Monday breakout of the prior-session range (weekly-open effect)",
    "source": "session-class:day-of-week (Monday open)",
}


def signal(ind, pos, htf=None):
    d = ind["dow"][pos]
    if nan(d) or int(d) != 0:        # Monday only
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
