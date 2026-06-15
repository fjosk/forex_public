#!/usr/bin/env python3
"""roc_momentum_breakout -- Rate of Change zero-cross with EMA200 trend filter. EarnForex."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "roc_momentum_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h/daily",
    "indicators": "roc, ema200, close",
    "long": "ROC crosses above zero AND close above ema200",
    "short": "ROC crosses below zero AND close below ema200",
    "desc": "ROC zero-cross momentum breakout with EMA200 trend filter",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """ROC zero-cross in trend direction: positive ROC momentum in uptrend."""
    if pos < 1:
        return None
    r0 = ind["roc"][pos]
    r1 = ind["roc"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(r0, r1, c, e200):
        return None

    if r0 > 0 and r1 <= 0 and c > e200:
        return "long"
    if r0 < 0 and r1 >= 0 and c < e200:
        return "short"

    return None
