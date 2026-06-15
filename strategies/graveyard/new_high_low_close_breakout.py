#!/usr/bin/env python3
"""new_high_low_close_breakout -- New N-period closing high/low trend-following breakout.
currency_trading_for_dummies_2nd_edition.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "new_high_low_close_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close prints a new N-period high (close > Donchian upper on close basis)",
    "short": "close prints a new N-period low (close < Donchian lower on close basis)",
    "desc": "New closing high/low trend-following breakout (Donchian-close)",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian",
}


def signal(ind, pos, htf=None):
    """Close exceeds prior N-bar Donchian high (new closing high) or breaks below (new closing low)."""
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
