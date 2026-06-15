#!/usr/bin/env python3
"""donchian_55_21_system -- 55-day entry breakout, 21-day exit breakout. trade_your_way_to_financial_freedom."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "55_21_day_channel_breakout_system",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low, close",
    "long": "close/high breaks above 55-day Donchian upper",
    "short": "close/low breaks below 55-day Donchian lower",
    "desc": "55/21-day dual-channel Donchian: 55-day entry, 21-day reverse extreme as trailing exit",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """55-day Donchian breakout entry; BREAK exit archetype handles the chandelier trail."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, c, dc_up, dc_lo):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
