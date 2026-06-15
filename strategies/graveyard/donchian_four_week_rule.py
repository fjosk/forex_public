#!/usr/bin/env python3
"""donchian_four_week_rule -- 4-week (20-bar) Donchian breakout; always-in stop-and-reverse. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_four_week_rule",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low, close",
    "long": "price exceeds the highest high of the prior 4 calendar weeks (~20 bars)",
    "short": "price falls below the lowest low of the prior 4 calendar weeks",
    "desc": "Donchian Four-Week Rule: always-in-market 20-bar Donchian breakout with stop-and-reverse",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """4-week Donchian breakout; TREND_FLIP = stop-and-reverse on opposite."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, h, l, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if l < dc_lo:
        return "short"
    return None
