#!/usr/bin/env python3
"""range_breakout_donchian -- Range breakout entry: close breaks above/below N-bar Donchian channel.
currency_trading_for_dummies_2nd_edition (stop-entry breakout).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "range_breakout_donchian",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close breaks above Donchian upper band (range high)",
    "short": "close breaks below Donchian lower band (range low)",
    "desc": "Range breakout via Donchian channel: close clears the prior horizontal range boundary",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian",
}


def signal(ind, pos, htf=None):
    """Close above/below prior Donchian band; signals a range breakout entry."""
    if pos < 1:
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
