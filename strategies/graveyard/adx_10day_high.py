#!/usr/bin/env python3
"""adx_10day_high -- ADX printing a 10-bar high signals fresh trend strength; enter with dominant DI. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "adx_10day_high",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus",
    "long": "ADX at 10-bar high and +DI>-DI",
    "short": "ADX at 10-bar high and -DI>+DI",
    "desc": "ADX printing a 10-bar high signals fresh trend strength; enter with dominant DI",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 9:
        return None
    adx = I['adx'][i]; dip = I['di_plus'][i]; dim = I['di_minus'][i]
    if _nan(adx, dip, dim):
        return None
    window = I['adx'][i-9:i+1]
    if any(_nan(v) for v in window):
        return None
    hi = max(window)
    if adx >= hi and dip > dim:
        return 'long'
    if adx >= hi and dim > dip:
        return 'short'
    return None
