#!/usr/bin/env python3
"""ema_momo_8_21 -- EMA MOMO 8/21 Crossover (TradersPost pinescript).
web:https://github.com/TradersPost/pinescript/blob/master/strategies/TradersPost%20Complex%20Example%20MOMO%20Strategy.pinescript
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_momo_8_21",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "ema8, ema21",
    "long": "ema8 crosses above ema21",
    "short": "ema8 crosses below ema21",
    "desc": "MOMO momentum strategy: fast EMA (8) vs slow EMA (21) crossover, both periods precomputed",
    "source": "web:https://github.com/TradersPost/pinescript/blob/master/strategies/TradersPost%20Complex%20Example%20MOMO%20Strategy.pinescript",
}


def signal(ind, pos, htf=None):
    """EMA8/EMA21 crossover in both directions."""
    e8 = ind["ema8"][pos]
    e21 = ind["ema21"][pos]
    e8_1 = ind["ema8"][pos - 1]
    e21_1 = ind["ema21"][pos - 1]
    if nan(e8, e21, e8_1, e21_1):
        return None
    if _xup(e8, e8_1, e21, e21_1):
        return "long"
    if _xdn(e8, e8_1, e21, e21_1):
        return "short"
    return None
