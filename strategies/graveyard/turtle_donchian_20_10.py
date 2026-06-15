#!/usr/bin/env python3
"""turtle_donchian_20_10 -- Turtle Trading: 20-bar entry / 10-bar exit Donchian. pplonski backtest."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_donchian_20_10",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, atr, close",
    "long": "close > 20-bar highest high (dc_up); symmetric short on dc_lo",
    "short": "close < 20-bar lowest low (dc_lo)",
    "desc": "Turtle Trading System 1: 20-bar Donchian breakout with 2xATR stop; pplonski Python backtest",
    "source": "web:https://github.com/pplonski/turtle-trading-python/blob/master/backtest.py",
}


def signal(ind, pos, htf=None):
    """Classic Turtle: break above dc_up or below dc_lo (prior bar, no look-ahead)."""
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
