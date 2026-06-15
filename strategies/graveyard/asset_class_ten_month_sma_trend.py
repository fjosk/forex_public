#!/usr/bin/env python3
"""asset_class_ten_month_sma_trend -- Asset Class Ten-Month SMA Trend Filter (Mebane Faber).
web:https://www.quantconnect.com/learning/articles/investment-strategy-library/asset-class-trend-following
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "asset_class_ten_month_sma_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "monthly",
    "indicators": "sma200, close",
    "long": "close > sma200 (above 10-month / 200-day SMA)",
    "short": "close < sma200 (below 200-day SMA; mirrored for FX)",
    "desc": "Mebane Faber 10-month SMA trend filter: long above 200-day SMA, short below",
    "source": "web:https://www.quantconnect.com/learning/articles/investment-strategy-library/asset-class-trend-following",
}


def signal(ind, pos, htf=None):
    """Long above sma200, short below; evaluated at each bar (engine cadence handles timing)."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    if nan(c, sma):
        return None
    if c > sma:
        return "long"
    if c < sma:
        return "short"
    return None
