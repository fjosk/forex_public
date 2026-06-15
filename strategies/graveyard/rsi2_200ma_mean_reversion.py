#!/usr/bin/env python3
"""rsi2_200ma_mean_reversion -- Connors RSI-2: SMA200 trend + RSI2 extreme. web:quantifiedstrategies.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_200ma_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "rsi2, sma200, close_sma5",
    "long": "close > sma200 AND rsi2 < 5",
    "short": "close < sma200 AND rsi2 > 95",
    "desc": "Connors RSI-2 mean reversion: SMA200 trend filter + RSI(2) extreme oversold/overbought",
    "source": "web:https://www.quantifiedstrategies.com/rsi-2-strategy/",
}


def signal(ind, pos, htf=None):
    """Larry Connors RSI-2 rule adapted for FX intraday: trend bias via SMA200, extreme RSI entry."""
    rsi2 = ind["rsi2"][pos]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(rsi2, s200, c):
        return None
    if c > s200 and rsi2 < 5:
        return "long"
    if c < s200 and rsi2 > 95:
        return "short"
    return None
