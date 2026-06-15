#!/usr/bin/env python3
"""resistance_breakout_donchian -- Range-break above resistance (consolidation high); Donchian proxy.
the_naked_trader.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "resistance_breakout_donchian",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, close",
    "long": "close decisively breaks above multi-period consolidation high (Donchian upper)",
    "short": "not specified (book is long-bias); engine will reverse on opposite break",
    "desc": "Resistance breakout: close clears the prior consolidation high (Donchian upper band)",
    "source": "book: the_naked_trader_how_anyone_can_still_make_money_t",
}


def signal(ind, pos, htf=None):
    """Close above prior Donchian upper (resistance breakout)."""
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
