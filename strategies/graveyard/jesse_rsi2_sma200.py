#!/usr/bin/env python3
"""jesse_rsi2_sma200 -- Jesse RSI(2) Mean Reversion with SMA200. jesse-ai example."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "jesse_rsi2_sma200",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "rsi2, sma200, close_sma5",
    "long": "close > sma200 AND rsi2 <= 10",
    "short": "close < sma200 AND rsi2 >= 90",
    "desc": "Larry Connors RSI(2) mean reversion with SMA200 regime filter (jesse-ai port)",
    "source": "github.com/jesse-ai/example-strategies RSI2/__init__.py",
}


def signal(ind, pos, htf=None):
    """RSI(2) extreme with SMA200 regime filter; exit on SMA5 cross."""
    c = ind["close"][pos]
    r2 = ind["rsi2"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, r2, s200):
        return None
    if c > s200 and r2 <= 10:
        return "long"
    if c < s200 and r2 >= 90:
        return "short"
    return None
