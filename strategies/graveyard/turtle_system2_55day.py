#!/usr/bin/env python3
"""turtle_system2_55day -- Turtle System 2: 55-bar Donchian breakout, no entry filter. Jesse AI."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_system2_55day",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, close, hh_n, ll_n, atr",
    "long": "close > 55-bar highest high (computed inline)",
    "short": "close < 55-bar lowest low (computed inline)",
    "desc": "Turtle System 2: 55-bar Donchian entry, 20-bar exit, no filter; slower trend system",
    "source": "web:https://github.com/jesse-ai/example-strategies/blob/master/TurtleRules/__init__.py",
}

_ENTRY_PERIOD = 55
_EXIT_PERIOD = 20


def signal(ind, pos, htf=None):
    """Turtle System 2: 55-bar high/low breakout computed inline."""
    c = ind["close"][pos]
    atr = ind["atr"][pos]
    if nan(c, atr):
        return None
    if pos < _ENTRY_PERIOD + 1:
        return None
    # Compute 55-bar channel inline (dc_up default period may be 20)
    hi55 = max(ind["high"][pos - _ENTRY_PERIOD:pos])
    lo55 = min(ind["low"][pos - _ENTRY_PERIOD:pos])
    if nan(hi55, lo55):
        return None
    if c > hi55:
        return "long"
    if c < lo55:
        return "short"
    return None
