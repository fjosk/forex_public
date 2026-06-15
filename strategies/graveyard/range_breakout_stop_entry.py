#!/usr/bin/env python3
"""range_breakout_stop_entry -- Range breakout via stop-loss entry orders: long on break of range high.
currency_trading_for_dummies_2nd_edition.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "range_breakout_stop_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high exceeds Donchian upper band (buy-stop triggers above range boundary)",
    "short": "low falls below Donchian lower band (sell-stop triggers below range boundary)",
    "desc": "Range breakout via stop-entry: high/low pokes through Donchian channel edge on the breakout bar",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian",
}


def signal(ind, pos, htf=None):
    """High or low pierces the prior Donchian band (stop-entry breakout)."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    lo = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, lo, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if lo < dc_lo:
        return "short"
    return None
