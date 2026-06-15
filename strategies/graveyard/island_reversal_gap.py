#!/usr/bin/env python3
"""island_reversal_gap -- twin-gap isolated-bar reversal: prior bar fully gapped away from its neighbours on both sides. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "island_reversal_gap",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ohlc",
    "long": "gap down into bar i-1 then gap up out of it (island bottom)",
    "short": "gap up into bar i-1 then gap down out of it (island top)",
    "desc": "twin-gap isolated-bar reversal: prior bar fully gapped away from its neighbours on both sides",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    h = I['high'][i]; l = I['low'][i]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    h2 = I['high'][i-2]; l2 = I['low'][i-2]
    if _nan(h, l, h1, l1, h2, l2):
        return None
    if (h1 < l2) and (l > h1):
        return 'long'
    if (l1 > h2) and (h < l1):
        return 'short'
    return None
