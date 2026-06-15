#!/usr/bin/env python3
"""ema_9_21_crossover_rsi_filter -- EMA 9/21 Crossover with RSI Zone Filter.
web:https://github.com/priyanshupriyank04/9-21_EMA_Crossover-RSI
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_9_21_crossover_rsi_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "ema9, ema21, rsi",
    "long": "ema9 crosses above ema21 AND 40 <= rsi <= 70",
    "short": "ema9 crosses below ema21 AND 30 <= rsi <= 60",
    "desc": "EMA 9/21 cross with RSI zone filter confirming momentum not at extremes",
    "source": "web:https://github.com/priyanshupriyank04/9-21_EMA_Crossover-RSI",
}


def signal(ind, pos, htf=None):
    """EMA9/EMA21 crossover gated by RSI zone: bullish 40-70, bearish 30-60."""
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e21_1 = ind["ema21"][pos - 1]
    rs = ind["rsi"][pos]
    if nan(e9, e21, e9_1, e21_1, rs):
        return None
    if _xup(e9, e9_1, e21, e21_1) and 40 <= rs <= 70:
        return "long"
    if _xdn(e9, e9_1, e21, e21_1) and 30 <= rs <= 60:
        return "short"
    return None
