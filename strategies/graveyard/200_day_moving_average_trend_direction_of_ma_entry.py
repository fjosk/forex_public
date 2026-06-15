#!/usr/bin/env python3
"""200_day_moving_average_trend_direction_of_ma_entry -- 200-day SMA slope turn: long when SMA200 rises, short when it falls. Alpha Trading Ch.5.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "200_day_moving_average_trend_direction_of_ma_entry",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma200",
    "long": "SMA200 slopes up: SMA200[i] > SMA200[i-1]",
    "short": "SMA200 slopes down: SMA200[i] < SMA200[i-1]",
    "desc": "200-day SMA slope turn signals trend direction; enter on the slope sign change",
    "source": "alpha_trading_profitable_strategies_that_remove_di Ch.5",
}


def signal(ind, pos, htf=None):
    """200-day MA direction: go with slope sign, reverse on flip."""
    if pos < 1:
        return None
    s = ind["sma200"][pos]
    s1 = ind["sma200"][pos - 1]
    if nan(s, s1):
        return None
    if s > s1:
        return "long"
    if s < s1:
        return "short"
    return None
