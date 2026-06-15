#!/usr/bin/env python3
"""short_break_below_support -- Short on close below Donchian lower support; long on close above resistance.
the_naked_trader.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "short_break_below_support",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_lo, dc_up, close",
    "long": "close breaks above Donchian upper (resistance breakout)",
    "short": "close breaks below Donchian lower (support breakdown -> short)",
    "desc": "Support breakdown short: close below multi-touch Donchian lower band triggers short entry",
    "source": "book: the_naked_trader_how_anyone_can_still_make_money_t",
}


def signal(ind, pos, htf=None):
    """Short on close below Donchian lower; long on close above Donchian upper."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    dc_lo = ind["dc_lo"][pos - 1]
    dc_up = ind["dc_up"][pos - 1]
    if nan(c, dc_lo, dc_up):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
