#!/usr/bin/env python3
"""channel_breakout_entry_opposite_stop -- 40-day entry Donchian, 10-day exit channel. trade_your_way_to_financial_freedom."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "channel_breakout_entry_with_opposite_channel_breakout_stop",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high makes a new 40-day Donchian upper breakout",
    "short": "low makes a new 40-day Donchian lower breakout",
    "desc": "40-day channel entry breakout with 10-day opposite channel as trailing exit (Tharp Ch.9)",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """40-day Donchian entry breakout; BREAK archetype handles trail/exit."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h >= dc_up:
        return "long"
    if l <= dc_lo:
        return "short"
    return None
