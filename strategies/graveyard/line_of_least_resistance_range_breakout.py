#!/usr/bin/env python3
"""line_of_least_resistance_range_breakout -- Donchian range breakout as the line of least resistance; wait for break to define direction. reminiscences_of_a_stock_operator."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "line_of_least_resistance_range_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, close",
    "long": "close crosses above Donchian upper (breaks above established range upper limit)",
    "short": "close falls below Donchian lower (breaks below established range lower limit)",
    "desc": "Line of least resistance: Donchian range breakout per Livermore; wait for the break to define direction",
    "source": "reminiscences_of_a_stock_operator_edwin_lefevre",
}


def signal(ind, pos, htf=None):
    """Close breaks above/below Donchian channel = line of least resistance established."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_up, dc_lo):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
