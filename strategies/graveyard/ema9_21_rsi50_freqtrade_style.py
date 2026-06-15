#!/usr/bin/env python3
"""ema9_21_rsi50_freqtrade_style -- EMA9/21 cross + RSI30-70 safety band. web:https://github.com/ynstf/Good-Freqtrade-Strategies"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema9_21_rsi50_freqtrade_style",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema9, ema21, rsi",
    "long": "ema9 crosses above ema21 AND rsi between 30 and 70",
    "short": "ema9 crosses below ema21 AND rsi between 30 and 70",
    "desc": "EMA9/21 cross with RSI momentum safety band (freqtrade community style, FX-adapted)",
    "source": "web:https://github.com/ynstf/Good-Freqtrade-Strategies",
}


def signal(ind, pos, htf=None):
    """EMA9/21 golden/death cross with RSI extremes filter."""
    e9 = ind["ema9"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e21 = ind["ema21"][pos]
    e21_1 = ind["ema21"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(e9, e9_1, e21, e21_1, rsi):
        return None
    rsi_safe = 30 < rsi < 70
    if _xup(e9, e9_1, e21, e21_1) and rsi_safe:
        return "long"
    if _xdn(e9, e9_1, e21, e21_1) and rsi_safe:
        return "short"
    return None
