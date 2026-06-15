#!/usr/bin/env python3
"""adx_surge_directional -- ADX surge with directional confirmation enters in dominant-DI direction. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "adx_surge_directional",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus",
    "long": "ADX rises >4 over 2 bars and +DI>-DI",
    "short": "ADX rises >4 over 2 bars and -DI>+DI",
    "desc": "ADX surge with directional confirmation enters in dominant-DI direction",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    adx = I['adx'][i]; adx2 = I['adx'][i-2]
    dip = I['di_plus'][i]; dim = I['di_minus'][i]
    if _nan(adx, adx2, dip, dim):
        return None
    if adx - adx2 > 4 and dip > dim:
        return 'long'
    if adx - adx2 > 4 and dim > dip:
        return 'short'
    return None
