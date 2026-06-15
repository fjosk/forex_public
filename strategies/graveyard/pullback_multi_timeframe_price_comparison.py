#!/usr/bin/env python3
"""pullback_multi_timeframe_price_comparison -- Multi-Timeframe Price Comparison Pullback.
web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/crude_oil.html
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pullback_multi_timeframe_price_comparison",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "close, open",
    "long": "bullish candle + below 200-bar close + above 20-bar close + below 10-bar close",
    "short": "bearish candle + above 200-bar close + below 20-bar close + above 10-bar close",
    "desc": "Four-condition multi-lookback pullback using raw price comparisons across 10/20/200 bars",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/crude_oil.html",
}


def signal(ind, pos, htf=None):
    """Multi-timeframe price comparison pullback: four conditions across 200/20/10 bar lookbacks."""
    if pos < 200:
        return None
    c = ind["close"][pos]
    o = ind["open"][pos]
    c10 = ind["close"][pos - 10]
    c20 = ind["close"][pos - 20]
    c200 = ind["close"][pos - 200]
    if nan(c, o, c10, c20, c200):
        return None
    if c > o and c < c200 and c > c20 and c < c10:
        return "long"
    if c < o and c > c200 and c < c20 and c > c10:
        return "short"
    return None
