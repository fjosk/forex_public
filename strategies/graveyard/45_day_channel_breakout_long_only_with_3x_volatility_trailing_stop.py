#!/usr/bin/env python3
"""channel_breakout_45day_long_only -- 45-day Donchian high breakout, long-only. trade_your_way_to_financial_freedom."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "45_day_channel_breakout_long_only_with_3x_volatility_trailing_stop",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "hh_n, dc_up",
    "long": "price makes a new 45-day highest high (Donchian upper breakout); long-only",
    "short": "no short side",
    "desc": "45-day channel breakout long-only with ATR chandelier trailing stop",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """Long only when current high exceeds 45-day Donchian upper (prior bars)."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    dc = ind["dc_up"][pos - 1]  # prior bar's Donchian upper (excludes current bar)
    if nan(h, dc):
        return None
    if h > dc:
        return "long"
    return None
