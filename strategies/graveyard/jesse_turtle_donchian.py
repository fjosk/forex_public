#!/usr/bin/env python3
"""jesse_turtle_donchian -- Classic Turtle System 1: 20-bar Donchian breakout. Jesse AI example."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "jesse_turtle_donchian",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, atr",
    "long": "close > dc_up (20-bar Donchian high)",
    "short": "close < dc_lo (20-bar Donchian low)",
    "desc": "Turtle System 1: 20-bar Donchian breakout with ATR stop, symmetric long/short",
    "source": "web:https://github.com/jesse-ai/example-strategies/blob/master/TurtleRules/__init__.py",
}


def signal(ind, pos, htf=None):
    """Enter on 20-bar Donchian channel breakout; exit handled by BREAK preset."""
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
