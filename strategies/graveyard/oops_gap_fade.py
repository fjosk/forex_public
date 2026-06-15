#!/usr/bin/env python3
"""oops_gap_fade -- Larry Williams Oops gap-fade: fade the exhaustion gap as price re-enters prior range. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_gap_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "open,high,low",
    "long": "Opens below prior low then trades back up into prior range",
    "short": "Opens above prior high then trades back down into prior range",
    "desc": "Larry Williams Oops gap-fade: fade the exhaustion gap as price re-enters prior range",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I['open'][i]; hi = I['high'][i]; lo = I['low'][i]
    hi1 = I['high'][i-1]; lo1 = I['low'][i-1]
    if _nan(o, hi, lo, hi1, lo1):
        return None
    if o < lo1 and hi >= lo1:
        return 'long'
    if o > hi1 and lo <= hi1:
        return 'short'
    return None
