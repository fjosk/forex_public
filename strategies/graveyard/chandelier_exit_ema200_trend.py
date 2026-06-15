#!/usr/bin/env python3
"""chandelier_exit_ema200_trend -- Chandelier Exit flip with EMA200 trend bias. Medium/Sword Red.

Long only when above EMA200 and chand_dir flips to +1. Short only when below EMA200 and
chand_dir flips to -1. The Chandelier Exit provides the trend-following entry trigger.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "chandelier_exit_ema200_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "chand_dir, ema200",
    "long": "chand_dir flips +1 and close > EMA200",
    "short": "chand_dir flips -1 and close < EMA200",
    "desc": "Chandelier Exit bullish/bearish flip with EMA200 directional filter",
    "source": "web:https://medium.com/@redsword_23261/chandelierexit-ema-dynamic-stop-loss-trend-following-strategy-4ed49f313a28",
}


def signal(ind, pos, htf=None):
    """Chandelier flip + EMA200 alignment."""
    cd = ind["chand_dir"][pos]
    cd1 = ind["chand_dir"][pos - 1]
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    if nan(cd, cd1, e200, c):
        return None
    if cd == 1 and cd1 == -1 and c > e200:
        return "long"
    if cd == -1 and cd1 == 1 and c < e200:
        return "short"
    return None
