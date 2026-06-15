#!/usr/bin/env python3
"""momentum_zero_line_trend_system -- n-day momentum (Close - Close[n]) zero-line cross: cross above = long; cross below = short. Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "momentum_zero_line_trend_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "roc, close",
    "long": "ROC crosses above zero (price momentum turns positive)",
    "short": "ROC crosses below zero (price momentum turns negative)",
    "desc": "Kaufman n-day momentum zero-cross trend system using ROC as proxy for Close-Close[n]",
    "source": "Kaufman, Trading Systems and Methods, Ch6 Momentum as a Trend Indicator, p.130-131, Fig 6-4",
}


def signal(ind, pos, htf=None):
    """ROC zero-cross as momentum trend signal."""
    if pos < 1:
        return None
    r = ind["roc"][pos]
    r1 = ind["roc"][pos - 1]
    if nan(r, r1):
        return None
    if _xup(r, r1, 0.0, 0.0):
        return "long"
    if _xdn(r, r1, 0.0, 0.0):
        return "short"
    return None
