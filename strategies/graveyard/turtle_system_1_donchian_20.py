#!/usr/bin/env python3
"""turtle_system_1_donchian_20 -- Turtle System 1: Donchian 20-day breakout entry. web:fundedtradingplus.com.

Go long on new 20-day high (close > dc_up[pos-1]); short on new 20-day low (close < dc_lo[pos-1]).
Exit on 10-day opposite breakout approximated with hh_n/ll_n rolling windows from high[]/low[].
No volume dependency.
"""
import numpy as np
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_system_1_donchian_20",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "dc_up, dc_lo, close, high, low",
    "long": "close > dc_up (20-day high breakout)",
    "short": "close < dc_lo (20-day low breakout)",
    "desc": "Turtle System 1: Donchian 20-day channel breakout entry",
    "source": "web:https://www.fundedtradingplus.com/propiq/turtle-trading-strategy-the-classic-breakout-system-made-simple-donchian-channels-trend-filter/",
}


def signal(ind, pos, htf=None):
    """Donchian 20-day breakout: close exceeds previous channel extreme."""
    c = ind["close"][pos]
    dc_hi = ind["dc_up"][pos - 1]   # prior-bar channel so current close breaks it fresh
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_hi, dc_lo):
        return None
    if c > dc_hi:
        return "long"
    if c < dc_lo:
        return "short"
    return None
