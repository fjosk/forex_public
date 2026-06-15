#!/usr/bin/env python3
"""ema_pair_crossover_generic -- EMA Pair Crossover Generic (AverageStrategy freqtrade).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AverageStrategy.py
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_pair_crossover_generic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "ema9, ema21",
    "long": "ema9 (short) crosses above ema21 (long); volume guard dropped for FX",
    "short": "ema9 crosses below ema21",
    "desc": "Parameterized EMA crossover; volume guard dropped (FX volume=0); ema9/ema21 as defaults",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AverageStrategy.py",
}


def signal(ind, pos, htf=None):
    """EMA9/EMA21 crossover; volume gate removed (FX volume always 0)."""
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e21_1 = ind["ema21"][pos - 1]
    if nan(e9, e21, e9_1, e21_1):
        return None
    if _xup(e9, e9_1, e21, e21_1):
        return "long"
    if _xdn(e9, e9_1, e21, e21_1):
        return "short"
    return None
