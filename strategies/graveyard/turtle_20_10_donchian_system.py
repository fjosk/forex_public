#!/usr/bin/env python3
"""turtle_20_10_donchian_system -- Turtle System 1: 20-bar entry, 10-bar exit Donchian. fxnx.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_20_10_donchian_system",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low, close, atr",
    "long": "close > dc_up[pos-1] (20-bar Donchian high breakout)",
    "short": "close < dc_lo[pos-1] (20-bar Donchian low breakout)",
    "desc": "Classic Turtle System 1: 20-bar Donchian entry, 10-bar exit, 2xATR stop",
    "source": "web:https://fxnx.com/en/blog/turtle-trading-algo-era-mastering-donchian-breakouts-modern",
}

_EXIT_PERIOD = 10


def signal(ind, pos, htf=None):
    """Turtle System 1: enter on 20-bar Donchian break, guarded by 10-bar exit inline check."""
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    atr = ind["atr"][pos]
    if nan(c, dc_up, dc_lo, atr):
        return None
    if pos < _EXIT_PERIOD + 2:
        return None
    # Compute inline 10-bar exit levels
    lo10 = min(ind["low"][pos - _EXIT_PERIOD:pos])
    hi10 = max(ind["high"][pos - _EXIT_PERIOD:pos])
    # Entry signals
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
