#!/usr/bin/env python3
"""rsi2_mean_reversion_daily -- RSI(2) deeply oversold/overbought mean reversion. QuantifiedStrategies."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_mean_reversion_daily",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "rsi2, close",
    "long": "RSI(2) < 10 (extreme oversold on daily)",
    "short": "RSI(2) > 90 (extreme overbought on daily)",
    "desc": "RSI(2) daily extreme mean reversion: enter on extreme RSI readings",
    "source": "web:https://quantifiedstrategies.substack.com/p/rsi-trading-strategies",
}


def signal(ind, pos, htf=None):
    """RSI(2) extreme mean reversion: deeply oversold = long, deeply overbought = short."""
    r2 = ind["rsi2"][pos]
    c = ind["close"][pos]
    if nan(r2, c):
        return None

    if r2 < 10:
        return "long"
    if r2 > 90:
        return "short"

    return None
