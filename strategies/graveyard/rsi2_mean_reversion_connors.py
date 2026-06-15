#!/usr/bin/env python3
"""rsi2_mean_reversion_connors -- Connors RSI(2) mean reversion in SMA200 trend. forextester.com.

RSI(2) extreme oversold/overbought within the SMA200 trend direction.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_mean_reversion_connors",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "rsi2, sma200",
    "long": "close > SMA200 (uptrend) AND RSI(2) < 10 (extreme oversold pullback)",
    "short": "close < SMA200 (downtrend) AND RSI(2) > 90 (extreme overbought rally)",
    "desc": "Connors RSI(2) mean reversion: extreme RSI dips in trend direction",
    "source": "https://forextester.com/blog/rsi-2-moving-averages-strategy/",
}


def signal(ind, pos, htf=None):
    """RSI(2) extreme dip/spike within SMA200 trend."""
    r2 = ind["rsi2"][pos]
    c = ind["close"][pos]
    ma200 = ind["sma200"][pos]
    if nan(r2, c, ma200):
        return None
    if c > ma200 and r2 < 10:
        return "long"
    if c < ma200 and r2 > 90:
        return "short"
    return None
