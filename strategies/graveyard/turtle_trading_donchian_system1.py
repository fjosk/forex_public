#!/usr/bin/env python3
"""turtle_trading_donchian_system1 -- Turtle System 1: 20-bar Donchian breakout. Jesse AI / gabekutner."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_trading_donchian_system1",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, atr, close",
    "long": "close > dc_up (20-bar Donchian high); symmetric short on dc_lo",
    "short": "close < dc_lo (20-bar Donchian low)",
    "desc": "Turtle System 1: 20-bar Donchian breakout with ATR stop; gabekutner/Jesse AI",
    "source": "web:https://github.com/jesse-ai/example-strategies/blob/master/TurtleRules/__init__.py",
}


def signal(ind, pos, htf=None):
    """Turtle System 1 entry: close breaks the prior bar Donchian channel."""
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    atr = ind["atr"][pos]
    if nan(c, dc_up, dc_lo, atr):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
