#!/usr/bin/env python3
"""donchian_channel_20day_breakout -- Donchian 20-day channel breakout (Turtle System 1). web:quantconnect.com."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_channel_20day_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > dc_up[pos-1] (breaks above prior 20-bar high)",
    "short": "close < dc_lo[pos-1] (breaks below prior 20-bar low)",
    "desc": "Donchian 20-day channel breakout -- Turtle System 1 / QuantConnect variant",
    "source": "web:https://www.quantconnect.com/forum/discussion/14220/donchian-channel-breakout-strategy/",
}


def signal(ind, pos, htf=None):
    """Classic 20-bar Donchian breakout: close vs prior bar channel boundary."""
    cl = ind["close"][pos]
    dcu1 = ind["dc_up"][pos - 1]
    dcl1 = ind["dc_lo"][pos - 1]
    if nan(cl, dcu1, dcl1):
        return None
    if cl > dcu1:
        return "long"
    if cl < dcl1:
        return "short"
    return None
