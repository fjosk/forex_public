#!/usr/bin/env python3
"""turtle_20_day_channel_breakout -- Turtle S1: new 20-bar high triggers long, new 20-bar low
triggers short. Classic Donchian channel entry.
Trade Your Way to Financial Freedom, Ch.7-8."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_20_day_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up,dc_lo,high,low",
    "long": "current high breaks above the 20-bar Donchian upper (new 20-bar high)",
    "short": "current low breaks below the 20-bar Donchian lower (new 20-bar low)",
    "desc": "Turtle System 1 Donchian 20-day channel breakout entry",
    "source": "Trade Your Way to Financial Freedom, Ch.7-8 (Turtles 20-day breakout reference)",
}


def signal(ind, pos, htf=None):
    """Turtle 20-day breakout: high > prior 20-bar high or low < prior 20-bar low."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_hi = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    if nan(h, l, dc_hi, dc_lo):
        return None
    if h > dc_hi:
        return "long"
    if l < dc_lo:
        return "short"
    return None
