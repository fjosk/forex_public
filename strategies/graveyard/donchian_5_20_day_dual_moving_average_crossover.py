#!/usr/bin/env python3
"""donchian_5_20_day_dual_moving_average_crossover -- Donchian 5/20-day SMA crossover stop-and-reverse system. Trade Your Way to Financial Freedom Ch.8.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_5_20_day_dual_moving_average_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close_sma5,sma20",
    "long": "SMA5 crosses above SMA20 (close_sma5 proxy)",
    "short": "SMA5 crosses below SMA20",
    "desc": "Donchian 5/20-day dual MA crossover; always in market, stop-and-reverse on opposite cross",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.8 Moving Averages",
}


def signal(ind, pos, htf=None):
    """5-bar SMA of close vs 20-bar SMA crossover."""
    if pos < 1:
        return None
    f = ind["close_sma5"][pos]
    f1 = ind["close_sma5"][pos - 1]
    s = ind["sma20"][pos]
    s1 = ind["sma20"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if f > s and f1 <= s1:
        return "long"
    if f < s and f1 >= s1:
        return "short"
    return None
