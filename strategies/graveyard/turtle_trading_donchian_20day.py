#!/usr/bin/env python3
"""turtle_trading_donchian_20day -- Turtle Trading 20-day Donchian breakout (classic forex adaptation). web:kritjunsree.medium.com.

Buy when current close exceeds the highest close of the prior 20 bars; sell when it is
the lowest close of the prior 20 bars. Uses dc_up/dc_lo (Donchian precomputed channel).
No volume dependency.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_trading_donchian_20day",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > dc_up (new 20-day high breakout)",
    "short": "close < dc_lo (new 20-day low breakout)",
    "desc": "Turtle Trading 20-day Donchian breakout (forex adaptation)",
    "source": "web:https://kritjunsree.medium.com/backtested-the-turtle-strategy-9fee0f0f5cb",
}


def signal(ind, pos, htf=None):
    """20-day Donchian channel breakout using precomputed dc_up/dc_lo."""
    c = ind["close"][pos]
    dc_hi = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    if nan(c, dc_hi, dc_lo):
        return None
    if c > dc_hi:
        return "long"
    if c < dc_lo:
        return "short"
    return None
