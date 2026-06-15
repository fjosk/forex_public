#!/usr/bin/env python3
"""macd_histogram_slope_trend_confirmation -- MACD-Histogram slope direction as trend confirmation: rising slope = long; falling slope = short. Elder.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_slope_trend_confirmation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd_hist",
    "long": "MACD-Histogram slope up: Hist(i) > Hist(i-1), bulls strengthening",
    "short": "MACD-Histogram slope down: Hist(i) < Hist(i-1), bears strengthening",
    "desc": "Elder MACD-H slope as trend direction confirmation: trade with the slope",
    "source": "Elder, Trading for a Living, Sec 26 MACD-Histogram Market Psychology, p.131-132",
}


def signal(ind, pos, htf=None):
    """MACD-Histogram slope direction as entry filter."""
    if pos < 1:
        return None
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    if nan(h, h1):
        return None
    if h > h1:
        return "long"
    if h < h1:
        return "short"
    return None
