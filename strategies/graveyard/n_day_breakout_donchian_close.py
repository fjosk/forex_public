#!/usr/bin/env python3
"""n_day_breakout_donchian_close -- N-day Donchian breakout: close-confirmed version.
trading_systems_and_methods_kaufman.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "n_day_breakout_donchian_close",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, dc_lo, high, low, close",
    "long": "high > prior N-bar Donchian high AND close > prior close",
    "short": "low < prior N-bar Donchian low AND close < prior close",
    "desc": "N-day Donchian channel breakout close-confirmed (always-in, stop-and-reverse)",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """High breaks prior Donchian high AND close confirms direction."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, lo, c, c1, dc_up, dc_lo):
        return None
    if h > dc_up and c > c1:
        return "long"
    if lo < dc_lo and c < c1:
        return "short"
    return None
