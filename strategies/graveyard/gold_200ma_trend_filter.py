#!/usr/bin/env python3
"""gold_200ma_trend_filter -- Gold SMA200 cross trend system (long-only bias). web:https://www.quantifiedstrategies.com/gold-moving-average-strategy/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "gold_200ma_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "sma200, sma50, close",
    "long": "close crosses above sma200 (gold MA filter), confirmed by sma50 > sma200",
    "short": "close crosses below sma200, sma50 < sma200 (death cross)",
    "desc": "Gold 200-day MA trend filter -- cross-above long, cross-below short with sma50 confirmation",
    "source": "web:https://www.quantifiedstrategies.com/gold-moving-average-strategy/",
}


def signal(ind, pos, htf=None):
    """SMA200 cross with sma50 golden/death cross confirmation."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    sma200 = ind["sma200"][pos]
    sma200_1 = ind["sma200"][pos - 1]
    sma50 = ind["sma50"][pos]
    if nan(c, c1, sma200, sma200_1, sma50):
        return None
    cross_above = c > sma200 and c1 <= sma200_1
    cross_below = c < sma200 and c1 >= sma200_1
    golden = sma50 > sma200
    death = sma50 < sma200
    if cross_above and golden:
        return "long"
    if cross_below and death:
        return "short"
    return None
