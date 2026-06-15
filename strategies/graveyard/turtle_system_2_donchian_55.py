#!/usr/bin/env python3
"""turtle_system_2_donchian_55 -- Turtle System 2: Donchian 55-day breakout entry. web:zayecapitalmarkets.com.

Go long when close exceeds the 55-bar rolling high; short when it drops below the 55-bar rolling low.
Uses hh_n and ll_n (rolling max/min over recent high/low arrays) as the 55-day Donchian proxy.
No volume dependency.
"""
import numpy as np
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_system_2_donchian_55",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "hh_n, ll_n, close, high, low",
    "long": "close breaks above 55-bar rolling high (hh_n)",
    "short": "close breaks below 55-bar rolling low (ll_n)",
    "desc": "Turtle System 2: 55-day Donchian breakout (long-term position)",
    "source": "web:https://zayecapitalmarkets.com/turtle-trading-strategy/",
}

_N = 55  # channel lookback


def signal(ind, pos, htf=None):
    """55-bar rolling high/low breakout entry."""
    c = ind["close"][pos]
    if nan(c):
        return None
    if pos < _N:
        return None
    hi_arr = ind["high"]
    lo_arr = ind["low"]
    window_hi = float(np.max(hi_arr[pos - _N:pos]))
    window_lo = float(np.min(lo_arr[pos - _N:pos]))
    if nan(window_hi, window_lo):
        return None
    if c > window_hi:
        return "long"
    if c < window_lo:
        return "short"
    return None
