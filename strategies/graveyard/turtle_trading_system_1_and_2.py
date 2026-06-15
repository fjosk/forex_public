#!/usr/bin/env python3
"""turtle_trading_system_1_and_2 -- Turtle Systems 1+2 combined: dc_up/dc_lo breakout. web:trendspider.com.

The combined Turtle rules using precomputed dc_up/dc_lo as the 20-day channel (System 1
proxy). System 2 would require 55-day inline; this module uses dc_up/dc_lo directly.
No volume dependency.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_trading_system_1_and_2",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "dc_up, dc_lo, close, atr",
    "long": "close breaks above dc_up (Donchian channel high)",
    "short": "close breaks below dc_lo (Donchian channel low)",
    "desc": "Turtle System 1+2 combined: Donchian channel breakout with ATR stop",
    "source": "web:https://trendspider.com/learning-center/richard-dennis-turtle-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Donchian channel breakout (System 1/2 combined proxy)."""
    c = ind["close"][pos]
    dc_hi = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_hi, dc_lo):
        return None
    if c > dc_hi:
        return "long"
    if c < dc_lo:
        return "short"
    return None
