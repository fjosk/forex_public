#!/usr/bin/env python3
"""roc_centerline_pullback_trend -- ROC centerline pullback in the direction of the EMA50/200 trend.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "roc_centerline_pullback_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "ROC, EMA50, EMA200",
    "long": "Uptrend (EMA50>EMA200), ROC was below zero and now turning up",
    "short": "Downtrend (EMA50<EMA200), ROC was above zero and now turning down",
    "desc": "ROC centerline pullback in the direction of the EMA50/200 trend.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e50, e200 = I["ema50"][i], I["ema200"][i]
    r, r1 = I["roc"][i], I["roc"][i-1]
    if _nan(e50, e200, r, r1):
        return None
    trend_up = e50 > e200
    if trend_up and r1 < 0 and r > r1:
        return "long"
    if (not trend_up) and r1 > 0 and r < r1:
        return "short"
    return None
