#!/usr/bin/env python3
"""outside_down_lower_open -- Williams open-relative fade: outside bar followed by a gap continuation open faded back against it. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "outside_down_lower_open",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ohlc",
    "long": "prior bar is an outside bar closing below the prior-low and today opens below prior close (exhaustion buy)",
    "short": "prior bar is an outside bar closing above the prior-high and today opens above prior close (exhaustion sell)",
    "desc": "Williams open-relative fade: outside bar followed by a gap continuation open faded back against it",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    o = I['open'][i]
    c1 = I['close'][i-1]; h1 = I['high'][i-1]; l1 = I['low'][i-1]
    h2 = I['high'][i-2]; l2 = I['low'][i-2]
    if _nan(o, c1, h1, l1, h2, l2):
        return None
    outside_down = h1 > h2 and l1 < l2 and c1 < l2
    if outside_down and o < c1:
        return 'long'
    outside_up = h1 > h2 and l1 < l2 and c1 > h2
    if outside_up and o > c1:
        return 'short'
    return None
