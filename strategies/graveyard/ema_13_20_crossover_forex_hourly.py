#!/usr/bin/env python3
"""ema_13_20_crossover_forex_hourly -- EMA 13/20 Crossover Forex Hourly (QuantConnect).
web:https://www.quantconnect.com/forum/discussion/4247/forex-ema-crossover-algo-py/
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_13_20_crossover_forex_hourly",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "ema13, ema20",
    "long": "ema13 crosses above ema20",
    "short": "ema13 crosses below ema20",
    "desc": "EMA 13/20 cross on forex hourly bars; both periods directly available in indicator set",
    "source": "web:https://www.quantconnect.com/forum/discussion/4247/forex-ema-crossover-algo-py/",
}


def signal(ind, pos, htf=None):
    """EMA13/EMA20 crossover; both periods are precomputed in the indicator set."""
    e13 = ind["ema13"][pos]
    e20 = ind["ema20"][pos]
    e13_1 = ind["ema13"][pos - 1]
    e20_1 = ind["ema20"][pos - 1]
    if nan(e13, e20, e13_1, e20_1):
        return None
    if _xup(e13, e13_1, e20, e20_1):
        return "long"
    if _xdn(e13, e13_1, e20, e20_1):
        return "short"
    return None
