#!/usr/bin/env python3
"""donchian_20_breakout -- Donchian 20-bar channel breakout. web:fxcc."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "donchian_20_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, atr",
    "long": "close breaks above prior bar dc_up (new 20-bar high)",
    "short": "close breaks below prior bar dc_lo (new 20-bar low)",
    "desc": "Classic Donchian 20-bar channel breakout: close above dc_up long, below dc_lo short",
    "source": "web:https://www.fxcc.com/donchian-channel-breakout-strategy",
}


def signal(ind, pos, htf=None):
    """Donchian 20-bar breakout."""
    c = ind["close"][pos]
    dc_up1 = ind["dc_up"][pos - 1]
    dc_lo1 = ind["dc_lo"][pos - 1]
    if nan(c, dc_up1, dc_lo1):
        return None
    if c > dc_up1:
        return "long"
    if c < dc_lo1:
        return "short"
    return None
