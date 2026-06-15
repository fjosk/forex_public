#!/usr/bin/env python3
"""macd_histogram_indicator_seasons -- MACD-Histogram four seasons: Spring (below zero, rising) = long; Autumn (above zero, falling) = short. Elder.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_indicator_seasons",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd_hist",
    "long": "MACD-Histogram below zero AND rising (Spring)",
    "short": "MACD-Histogram above zero AND falling (Autumn)",
    "desc": "Elder Indicator Seasons: Spring = histogram below zero and ticking up -> long; Autumn = above zero ticking down -> short",
    "source": "Elder, Trading for a Living, Sec 36 Indicator Seasons, Fig 36-2",
}


def signal(ind, pos, htf=None):
    """MACD-Histogram seasons: Spring->long, Autumn->short."""
    if pos < 1:
        return None
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    if nan(h, h1):
        return None
    # Spring: below zero and rising
    if h < 0 and h > h1:
        return "long"
    # Autumn: above zero and falling
    if h > 0 and h < h1:
        return "short"
    return None
