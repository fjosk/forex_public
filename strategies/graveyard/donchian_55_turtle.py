#!/usr/bin/env python3
"""donchian_55_turtle -- 55-bar Donchian breakout with chandelier exit (Turtle Alt31). web:github/trustdan."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "donchian_55_turtle",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, chand_dir",
    "long": "close breaks above 55-bar Donchian upper band (dc_up on prior bar)",
    "short": "close breaks below 55-bar Donchian lower band (dc_lo on prior bar)",
    "desc": "55-bar Donchian Turtle breakout with chandelier trailing stop direction (trustdan Alt31)",
    "source": "web:https://github.com/trustdan/trend-following-backtesting-strategies",
}


def signal(ind, pos, htf=None):
    """55-bar Donchian breakout: close vs prior bar dc_up/dc_lo."""
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
