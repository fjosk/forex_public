#!/usr/bin/env python3
"""roc_momentum_zero_cross -- Rate of Change zero-line crossover with SMA200 filter. QuantifiedStrategies.

ROC crosses from negative to positive (long) or positive to negative (short).
SMA200 trend filter reduces noise by aligning trade direction with the dominant trend.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "roc_momentum_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "roc, sma200",
    "long": "ROC crosses above zero and close > SMA200",
    "short": "ROC crosses below zero and close < SMA200",
    "desc": "Rate of Change zero-line crossover with SMA200 trend alignment",
    "source": "web:https://www.quantifiedstrategies.com/rate-of-change-trading-strategy/",
}

_ZERO = 0.0


def signal(ind, pos, htf=None):
    """ROC zero-cross with SMA200 filter."""
    roc = ind["roc"][pos]
    roc1 = ind["roc"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(roc, roc1, s200, c):
        return None
    if _xup(roc, roc1, _ZERO, _ZERO) and c > s200:
        return "long"
    if _xdn(roc, roc1, _ZERO, _ZERO) and c < s200:
        return "short"
    return None
