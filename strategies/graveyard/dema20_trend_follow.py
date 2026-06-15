#!/usr/bin/env python3
"""dema20_trend_follow -- DEMA(20) price cross trend filter. web:https://www.alphatechfinance.com/investing-etfs/ema-exponential-moving-average-trading-guide-2025/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dema20_trend_follow",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "dema20, atr",
    "long": "close crosses above dema20 AND dema20 rising",
    "short": "close crosses below dema20 AND dema20 falling",
    "desc": "DEMA(20) price cross trend filter with slope confirmation",
    "source": "web:https://www.alphatechfinance.com/investing-etfs/ema-exponential-moving-average-trading-guide-2025/",
}


def signal(ind, pos, htf=None):
    """DEMA(20) cross with slope filter."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    d = ind["dema20"][pos]
    d1 = ind["dema20"][pos - 1]
    if nan(c, c1, d, d1):
        return None
    cross_above = c > d and c1 <= d1
    cross_below = c < d and c1 >= d1
    dema_rising = d > d1
    dema_falling = d < d1
    if cross_above and dema_rising:
        return "long"
    if cross_below and dema_falling:
        return "short"
    return None
