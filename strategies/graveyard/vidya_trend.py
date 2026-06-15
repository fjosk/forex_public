#!/usr/bin/env python3
"""vidya_trend -- Volatility-adaptive VIDYA line turning up or down by an ATR-scaled threshold. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "vidya_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "vidya,atr",
    "long": "Chande VIDYA rises more than 0.10 ATR over one bar",
    "short": "Chande VIDYA falls more than 0.10 ATR over one bar",
    "desc": "Volatility-adaptive VIDYA line turning up or down by an ATR-scaled threshold",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    v, v1, a = I["vidya"][i], I["vidya"][i-1], I["atr"][i]
    if _nan(v, v1, a):
        return None
    band = 0.10 * a
    if v - v1 > band:
        return "long"
    if v - v1 < -band:
        return "short"
    return None
