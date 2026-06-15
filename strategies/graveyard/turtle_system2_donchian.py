#!/usr/bin/env python3
"""turtle_system2_donchian -- Turtle System 2 Donchian 55-day breakout (canonical). web:ig.com.

Classic Dennis/Eckhardt System 2: enter on 55-day new high/low breakout; exit driven by
the engine's BREAK exit archetype. Uses rolling 55-bar high/low inline from high[]/low[].
No volume dependency.
"""
import numpy as np
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_system2_donchian",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "close, high, low",
    "long": "close breaks above highest high of last 55 bars",
    "short": "close breaks below lowest low of last 55 bars",
    "desc": "Turtle System 2 Donchian 55-day breakout (Dennis/Eckhardt canonical)",
    "source": "web:https://www.ig.com/en/trading-strategies/turtle-trading--what-is-it-and-what-are-the-rules--180904",
}

_N = 55


def signal(ind, pos, htf=None):
    """55-bar new high/low breakout for Turtle System 2."""
    c = ind["close"][pos]
    if nan(c) or pos < _N:
        return None
    hi = ind["high"]
    lo = ind["low"]
    ch_hi = float(np.max(hi[pos - _N:pos]))
    ch_lo = float(np.min(lo[pos - _N:pos]))
    if nan(ch_hi, ch_lo):
        return None
    if c > ch_hi:
        return "long"
    if c < ch_lo:
        return "short"
    return None
