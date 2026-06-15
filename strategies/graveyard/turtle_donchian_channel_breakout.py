#!/usr/bin/env python3
"""turtle_donchian_channel_breakout -- Turtle Donchian 20-bar breakout (Richard Dennis / Eckhardt).

Long when close breaks above the prior bar's 20-bar Donchian high (dc_up).
Short when close breaks below the prior bar's 20-bar Donchian low (dc_lo).
Classic Turtle System 1 entry; no pyramiding in this single-unit implementation.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_donchian_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "daily",
    "indicators": "dc_up, dc_lo, atr",
    "long": "close breaks above prior bar dc_up (20-bar high)",
    "short": "close breaks below prior bar dc_lo (20-bar low)",
    "desc": "Turtle Donchian Channel 20-bar breakout (System 1)",
    "source": "web:https://alchemymarkets.com/education/strategies/turtle-trading-guide/; Curtis Faith (2003)",
}


def signal(ind, pos, htf=None):
    """Donchian breakout: close crosses prior dc_up/dc_lo."""
    c = ind["close"][pos]
    dc_up_1 = ind["dc_up"][pos - 1]
    dc_lo_1 = ind["dc_lo"][pos - 1]
    if nan(c, dc_up_1, dc_lo_1):
        return None
    if c > dc_up_1:
        return "long"
    if c < dc_lo_1:
        return "short"
    return None
