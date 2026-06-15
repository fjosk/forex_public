#!/usr/bin/env python3
"""ema5_ema12_rsi21_crossover -- EMA5/8 cross with RSI momentum filter. web:https://www.forexfactory.com/thread/599061-simple-rsi-ema-high-profitable-ratio-strategy"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema5_ema12_rsi21_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema8, rsi",
    "long": "ema5 crosses above ema8 AND rsi > 50",
    "short": "ema5 crosses below ema8 AND rsi < 50",
    "desc": "EMA5/EMA8 crossover with RSI50 momentum filter (ema8 proxies ema12)",
    "source": "web:https://www.forexfactory.com/thread/599061-simple-rsi-ema-high-profitable-ratio-strategy",
}


def signal(ind, pos, htf=None):
    """EMA5 crosses EMA8 (proxy for ema12) with RSI50 filter."""
    e5 = ind["ema5"][pos]
    e5_1 = ind["ema5"][pos - 1]
    e8 = ind["ema8"][pos]
    e8_1 = ind["ema8"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(e5, e5_1, e8, e8_1, rsi):
        return None
    if _xup(e5, e5_1, e8, e8_1) and rsi > 50:
        return "long"
    if _xdn(e5, e5_1, e8, e8_1) and rsi < 50:
        return "short"
    return None
