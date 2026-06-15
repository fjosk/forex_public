#!/usr/bin/env python3
"""donchian_channel_breakout -- Donchian channel breakout (zeta-zetra Python, 72-bar). web:github.com/zeta-zetra."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > dc_up[pos-1] (prior Donchian upper band)",
    "short": "close < dc_lo[pos-1] (prior Donchian lower band)",
    "desc": "Donchian channel breakout (zeta-zetra, 72-bar period): close vs prior channel boundary",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Donchian channel breakout: close vs prior-bar channel boundary."""
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
