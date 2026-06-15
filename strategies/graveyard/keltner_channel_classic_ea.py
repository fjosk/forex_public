#!/usr/bin/env python3
"""keltner_channel_classic_ea -- Classic Keltner Channel breakout EA. MQL5 blog / 2020.

Enter long when close crosses above kc_up; enter short when close crosses below kc_lo. The
engine's BREAK exit archetype (ATR trailing stop) replaces the fixed SL/TP points from the
original MQL4 EA.
"""
from strategies._common import nan, BREAK, ALL_CLASSES, _xup, _xdn

META = {
    "id": "keltner_channel_classic_ea",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "kc_up, kc_lo, kc_mid, close",
    "long": "close crosses above kc_up (price breaks above upper Keltner band)",
    "short": "close crosses below kc_lo (price breaks below lower Keltner band)",
    "desc": "Classic Keltner Channel breakout: close crosses outer band; ATR trailing stop exit",
    "source": "https://www.mql5.com/en/blogs/post/734150 (Classic Keltner Channel EA example)",
}


def signal(ind, pos, htf=None):
    """Keltner Channel band breakout entry."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    if nan(c, c1, kc_up, kc_lo, kc_up1, kc_lo1):
        return None
    if _xup(c, c1, kc_up, kc_up1):
        return "long"
    if _xdn(c, c1, kc_lo, kc_lo1):
        return "short"
    return None
