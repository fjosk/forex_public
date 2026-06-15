#!/usr/bin/env python3
"""ma_crossover_mean_reversion -- Moving Average Cross Mean Reversion. armelf Financial-Algorithms."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ma_crossover_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma20, sma50, sma200",
    "long": "sma20 crosses above sma50 AND close > sma200 (uptrend regime)",
    "short": "sma20 crosses below sma50 AND close < sma200 (downtrend regime)",
    "desc": "SMA20/SMA50 crossover with SMA200 trend regime filter; exit on reverse cross",
    "source": "github.com/armelf/Financial-Algorithms MA Cross strategy",
}


def signal(ind, pos, htf=None):
    """SMA20/50 cross in direction of SMA200 regime."""
    s20 = ind["sma20"][pos]
    s201 = ind["sma20"][pos - 1]
    s50 = ind["sma50"][pos]
    s501 = ind["sma50"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(s20, s201, s50, s501, s200, c):
        return None
    if _xup(s20, s201, s50, s501) and c > s200:
        return "long"
    if _xdn(s20, s201, s50, s501) and c < s200:
        return "short"
    return None
