#!/usr/bin/env python3
"""n_day_channel_close_penetration -- N-day price channel: signal on close penetration of prior high/low.
trading_systems_and_methods_kaufman.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "n_day_channel_close_penetration",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > max(high) of prior N days (Donchian upper)",
    "short": "close < min(low) of prior N days (Donchian lower)",
    "desc": "Closing-price channel breakout: close penetrates Donchian upper/lower band; always-in",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Close breaches prior Donchian band (close-only filter)."""
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
