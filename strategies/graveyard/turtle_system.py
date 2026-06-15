#!/usr/bin/env python3
"""turtle_system -- Turtle Trading System 2 (55-day Donchian breakout). web:tradingblox."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "turtle_system",
    "cadences": ["swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, hh_n, ll_n, atr",
    "long": "close breaks above 20-bar Donchian high (S1 entry, always taken as S2 approximation)",
    "short": "close breaks below 20-bar Donchian low",
    "desc": "Turtle Trading System breakout using Donchian channel with ATR-based stops",
    "source": "web:https://www.tradingblox.com/Manuals/UsersGuideHTML/turtlesystem.htm",
}


def signal(ind, pos, htf=None):
    """Turtle system Donchian breakout (S1: dc_up/dc_lo)."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    dc_up1 = ind["dc_up"][pos - 1]
    dc_lo1 = ind["dc_lo"][pos - 1]
    atr = ind["atr"][pos]
    if nan(c, c1, dc_up, dc_lo, dc_up1, dc_lo1, atr):
        return None
    # S1 entry: break above prior bar's channel (crossover)
    if c > dc_up1 and c1 <= dc_up1:
        return "long"
    if c < dc_lo1 and c1 >= dc_lo1:
        return "short"
    return None
