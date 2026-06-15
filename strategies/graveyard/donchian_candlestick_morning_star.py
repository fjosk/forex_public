#!/usr/bin/env python3
"""donchian_candlestick_morning_star -- Morning/Evening Star reversal at Donchian extremes. web:zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "donchian_candlestick_morning_star",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "dc_lo, dc_up, open, close, high, low",
    "long": "3-bar Morning Star at/near dc_lo: bearish bar, small body, bullish engulf; close above Morning Star high",
    "short": "3-bar Evening Star at/near dc_up: bullish bar, small body, bearish engulf; close below Evening Star low",
    "desc": "Donchian Channel morning/evening star reversal at channel extremes (zeta-zetra)",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/chatgpt/donchian_channel_candlestick.html",
}


def signal(ind, pos, htf=None):
    """3-bar morning/evening star reversal at Donchian channel extremes."""
    if pos < 2:
        return None
    cl = ind["close"][pos]
    op = ind["open"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    cl1 = ind["close"][pos - 1]
    op1 = ind["open"][pos - 1]
    cl2 = ind["close"][pos - 2]
    op2 = ind["open"][pos - 2]
    lo2 = ind["low"][pos - 2]
    hi2 = ind["high"][pos - 2]
    dcl = ind["dc_lo"][pos]
    dcu = ind["dc_up"][pos]
    if nan(cl, op, hi, lo, cl1, op1, cl2, op2, lo2, hi2, dcl, dcu):
        return None
    body2 = abs(cl2 - op2)
    body1 = abs(cl1 - op1)
    # Morning Star (long): bearish bar2, small body bar1, bullish bar0 near dc_lo
    near_lower = lo2 <= dcl or lo <= dcl
    bar2_bearish = cl2 < op2
    bar1_small = body2 > 0 and body1 < 0.3 * body2
    bar0_bullish = cl > op and cl > (cl2 + op2) / 2.0
    if near_lower and bar2_bearish and bar1_small and bar0_bullish and cl > hi2:
        return "long"
    # Evening Star (short): bullish bar2, small body bar1, bearish bar0 near dc_up
    near_upper = hi2 >= dcu or hi >= dcu
    bar2_bullish = cl2 > op2
    bar0_bearish = cl < op and cl < (cl2 + op2) / 2.0
    if near_upper and bar2_bullish and bar1_small and bar0_bearish and cl < lo2:
        return "short"
    return None
