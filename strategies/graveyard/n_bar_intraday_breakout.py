#!/usr/bin/env python3
"""n_bar_intraday_breakout -- N-bar Donchian channel breakout applied on intraday bars.
trading_systems_and_methods_kaufman.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "n_bar_intraday_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high breaks above N-bar Donchian highest high",
    "short": "low breaks below N-bar Donchian lowest low",
    "desc": "N-bar Donchian channel breakout (stop-and-reverse always in market)",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Price breaks above/below prior Donchian channel; reverse on opposite."""
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
