#!/usr/bin/env python3
"""macd_hist_seasons -- MACD-histogram indicator-seasons quadrant entry.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "macd_hist_seasons",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MACD(12,26,9) histogram",
    "long": "Histogram below zero and rising (Spring quadrant)",
    "short": "Histogram above zero and falling (Autumn quadrant)",
    "desc": "MACD-histogram indicator-seasons quadrant entry.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    hh, h1 = I["macd_hist"][i], I["macd_hist"][i-1]
    if _nan(hh, h1):
        return None
    rising = hh > h1
    if hh < 0 and rising:
        return "long"
    if hh > 0 and not rising:
        return "short"
    return None
