#!/usr/bin/env python3
"""three_up_close_fade -- consecutive-close-count exhaustion fade with a close-beyond-prior-extreme stretch trigger. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "three_up_close_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ohlc",
    "long": "three lower closes in a row then a close below prior low -> fade long",
    "short": "three higher closes in a row then a close above prior high -> fade short",
    "desc": "consecutive-close-count exhaustion fade with a close-beyond-prior-extreme stretch trigger",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 3:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]; c2 = I['close'][i-2]; c3 = I['close'][i-3]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    if _nan(c, c1, c2, c3, h1, l1):
        return None
    long_run = c > c1 and c1 > c2 and c2 > c3
    if long_run and c > h1:
        return 'short'
    short_run = c < c1 and c1 < c2 and c2 < c3
    if short_run and c < l1:
        return 'long'
    return None
