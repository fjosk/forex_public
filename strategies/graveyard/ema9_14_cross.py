#!/usr/bin/env python3
"""ema9_14_cross -- EMA9/EMA20 crossover (ema20 proxies ema14). web:https://www.earnforex.com/forex-strategy/moving-average-cross-strategy/"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema9_14_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema9, ema20",
    "long": "ema9 crosses above ema20",
    "short": "ema9 crosses below ema20",
    "desc": "EMA9/EMA20 crossover trend follower (ema20 proxies the spec ema14)",
    "source": "web:https://www.earnforex.com/forex-strategy/moving-average-cross-strategy/",
}


def signal(ind, pos, htf=None):
    """EMA9 crosses EMA20 (closest available proxy for EMA14)."""
    e9 = ind["ema9"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    if nan(e9, e9_1, e20, e20_1):
        return None
    if _xup(e9, e9_1, e20, e20_1):
        return "long"
    if _xdn(e9, e9_1, e20, e20_1):
        return "short"
    return None
