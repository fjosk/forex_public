#!/usr/bin/env python3
"""donchian_10_20_moving_average_crossover -- Donchian 10/20 SMA crossover: long when SMA10 crosses above SMA20. Trade Your Way to Financial Freedom Ch.1.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_10_20_moving_average_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma10,sma20",
    "long": "SMA10 crosses above SMA20",
    "short": "SMA10 crosses below SMA20",
    "desc": "Donchian 10/20 SMA crossover; always in market, reverses on opposite cross",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.1 Ed Seykota",
}


def signal(ind, pos, htf=None):
    """SMA10 vs SMA20 crossover."""
    if pos < 1:
        return None
    f = ind["sma10"][pos]
    f1 = ind["sma10"][pos - 1]
    s = ind["sma20"][pos]
    s1 = ind["sma20"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if f > s and f1 <= s1:
        return "long"
    if f < s and f1 >= s1:
        return "short"
    return None
