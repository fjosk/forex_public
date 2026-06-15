#!/usr/bin/env python3
"""donchian_channel_breakout_turtle_20_40_55 -- Turtle Donchian entry breakout (20/40/55-day); shorter exit channel. trade_your_way_to_financial_freedom."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "donchian_channel_breakout_turtle_20_40_55_day",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high breaks above the N-day Donchian upper (default N matches dc_up parameter)",
    "short": "low breaks below the N-day Donchian lower",
    "desc": "Turtle Donchian channel breakout (20/40/55-day entry); BREAK exit archetype handles trail",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """Donchian breakout; engine dc_up/dc_lo parameter controls lookback."""
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
