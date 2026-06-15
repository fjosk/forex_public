#!/usr/bin/env python3
"""lambert_mdi_cross -- Lambert Market Direction Indicator zero-line cross: short-term price change normalized by the average price flips sign.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "lambert_mdi_cross",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MDI (Lambert Market Direction Indicator)",
    "long": "MDI crosses above zero",
    "short": "MDI crosses below zero",
    "desc": "Lambert Market Direction Indicator zero-line cross: short-term price change normalized by the average price flips sign.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    m, m1 = I["mdi"][i], I["mdi"][i-1]
    if _nan(m, m1):
        return None
    if m > 0 and m1 <= 0:
        return "long"
    if m < 0 and m1 >= 0:
        return "short"
    return None
