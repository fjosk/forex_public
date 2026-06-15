#!/usr/bin/env python3
"""donchian_turtle_breakout -- Donchian Turtle System 1 (20-bar) breakout. web:altrady."""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "donchian_turtle_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, atr",
    "long": "close crosses above 20-bar Donchian high (System 1 buy)",
    "short": "close crosses below 20-bar Donchian low (System 1 sell)",
    "desc": "Turtle Trading System 1: 20-bar Donchian channel breakout crossover",
    "source": "web:https://www.altrady.com/blog/crypto-trading-strategies/turtle-trading-strategy-rules",
}


def signal(ind, pos, htf=None):
    """Turtle System 1: 20-bar Donchian crossover."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    dc_up1 = ind["dc_up"][pos - 1]
    dc_lo1 = ind["dc_lo"][pos - 1]
    if nan(c, c1, dc_up, dc_lo, dc_up1, dc_lo1):
        return None
    if _xup(c, c1, dc_up, dc_up1):
        return "long"
    if _xdn(c, c1, dc_lo, dc_lo1):
        return "short"
    return None
