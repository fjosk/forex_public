#!/usr/bin/env python3
"""dual_moving_average_crossover_9_21 -- EMA9/EMA21 dual moving-average crossover. Currency Trading for Dummies Ch.11.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dual_moving_average_crossover_9_21",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema9,ema21",
    "long": "EMA9 crosses above EMA21",
    "short": "EMA9 crosses below EMA21",
    "desc": "9/21 EMA dual crossover; always in market, reverses on opposite cross",
    "source": "currency_trading_for_dummies_2nd_edition_by_brian Ch.11 Moving Averages",
}


def signal(ind, pos, htf=None):
    """EMA9 vs EMA21 crossover."""
    if pos < 1:
        return None
    f = ind["ema9"][pos]
    f1 = ind["ema9"][pos - 1]
    s = ind["ema21"][pos]
    s1 = ind["ema21"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if f > s and f1 <= s1:
        return "long"
    if f < s and f1 >= s1:
        return "short"
    return None
