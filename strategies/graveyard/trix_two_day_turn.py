#!/usr/bin/env python3
"""trix_two_day_turn -- Two-bar TRIX direction confirmation for momentum-aligned entries. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "trix_two_day_turn",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "trix",
    "long": "TRIX rising two bars in a row",
    "short": "TRIX falling two bars in a row",
    "desc": "Two-bar TRIX direction confirmation for momentum-aligned entries",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    t = I['trix'][i]; t1 = I['trix'][i-1]; t2 = I['trix'][i-2]
    if _nan(t, t1, t2):
        return None
    if t > t1 and t1 > t2:
        return 'long'
    if t < t1 and t1 < t2:
        return 'short'
    return None
