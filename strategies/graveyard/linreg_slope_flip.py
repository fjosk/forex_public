#!/usr/bin/env python3
"""linreg_slope_flip -- Least-squares 20-bar regression slope sign flip marks the trend turn. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "linreg_slope_flip",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "lrs20",
    "long": "Linear-regression slope of close over 20 bars crosses up through zero",
    "short": "Linear-regression slope of close over 20 bars crosses down through zero",
    "desc": "Least-squares 20-bar regression slope sign flip marks the trend turn",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    s, s1 = I["lrs20"][i], I["lrs20"][i-1]
    if _nan(s, s1):
        return None
    if s > 0 and s1 <= 0:
        return "long"
    if s < 0 and s1 >= 0:
        return "short"
    return None
