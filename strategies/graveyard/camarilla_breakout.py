#!/usr/bin/env python3
"""camarilla_breakout -- breakout beyond the Camarilla H4/L4 levels. Session class."""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "camarilla_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "cam_r4, cam_s4, close",
    "long": "close crosses above the Camarilla R4 breakout level",
    "short": "close crosses below the Camarilla S4 breakout level",
    "desc": "Camarilla H4/L4 daily breakout",
    "source": "session-class:Camarilla pivots",
}


def signal(ind, pos, htf=None):
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    r4, s4 = ind["cam_r4"][pos], ind["cam_s4"][pos]
    if nan(c, c1, r4, s4):
        return None
    if _xup(c, c1, r4, r4):
        return "long"
    if _xdn(c, c1, s4, s4):
        return "short"
    return None
