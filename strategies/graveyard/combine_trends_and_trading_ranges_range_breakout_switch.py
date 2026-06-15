#!/usr/bin/env python3
"""combine_trends_trading_ranges_switch -- Range/trend switch: inside range use MA direction, on breakout follow trend. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "combine_trends_and_trading_ranges_range_breakout_switch",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "sma20, dc_up, dc_lo, close, sma200_dir",
    "long": "price breaks above Donchian upper resistance (upside breakout) AND sma20 slope up",
    "short": "price breaks below Donchian lower support (downside breakout) AND sma20 slope down",
    "desc": "Range-breakout switch: enter on Donchian breakout confirmed by MA direction; ignore range interior",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Donchian breakout with MA slope confirmation; ignores trades inside the range."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    ma = ind["sma20"]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    ma_cur = ma[pos]
    ma_prev = ma[pos - 1]
    if nan(c, dc_up, dc_lo, ma_cur, ma_prev):
        return None
    ma_up = ma_cur > ma_prev
    ma_dn = ma_cur < ma_prev
    if c > dc_up and ma_up:
        return "long"
    if c < dc_lo and ma_dn:
        return "short"
    return None
