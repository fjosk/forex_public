#!/usr/bin/env python3
"""donchian_55_21_turtle_style -- 55-day entry channel / 21-day exit channel, Turtle-style always-in. trade_your_way_to_financial_freedom."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "55_21_day_channel_breakout_system_turtle_style",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, hh_n, ll_n, high, low",
    "long": "price makes a new 55-day high (dc_up breakout)",
    "short": "price makes a new 55-day low (dc_lo breakout)",
    "desc": "55/21-day Donchian channel breakout Turtle-style; 55-day entry, exit on opposite signal",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """55-day Donchian entry breakout, stop-and-reverse on opposing signal."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if l < dc_lo:
        return "short"
    return None
