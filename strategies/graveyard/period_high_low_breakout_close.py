#!/usr/bin/env python3
"""period_high_low_breakout_close -- Period high/low close-confirmed breakout.
currency_trading_for_dummies_2nd_edition.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "period_high_low_breakout_close",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "period close finishes above most recent significant period high (Donchian upper)",
    "short": "period close finishes below most recent significant period low (Donchian lower)",
    "desc": "Period high/low breakout requiring a close beyond the level (not just intrabar touch)",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian",
}


def signal(ind, pos, htf=None):
    """Close exceeds prior-period Donchian band (close-confirmed)."""
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
