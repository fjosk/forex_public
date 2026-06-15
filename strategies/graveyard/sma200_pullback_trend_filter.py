#!/usr/bin/env python3
"""sma200_pullback_trend_filter -- SMA200 pullback: trade reversion back to the MA. web:tradingwithrayner.com.

Price above SMA200 = longs only; below = shorts only. Entry when price pulls back to
within 0.2% of SMA200 and closes on the correct side (dynamic support/resistance test).
No volume dependency.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "sma200_pullback_trend_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "sma200, close",
    "long": "close > sma200 AND close within 0.2% of sma200 (pullback to support)",
    "short": "close < sma200 AND close within 0.2% of sma200 (pullback to resistance)",
    "desc": "SMA200 pullback: price retraces to the 200 MA in the trend direction",
    "source": "web:https://www.tradingwithrayner.com/200-day-moving-average/",
}


def signal(ind, pos, htf=None):
    """Enter when price pulls back close to SMA200 in the trend direction."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    if nan(c, sma) or sma == 0:
        return None
    proximity = abs(c - sma) / sma
    if proximity > 0.002:
        return None
    if c > sma:
        return "long"
    if c < sma:
        return "short"
    return None
