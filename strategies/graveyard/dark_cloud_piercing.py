#!/usr/bin/env python3
"""dark_cloud_piercing -- two-candle partial-penetration reversal needing a gap then a close past the prior body midpoint. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "dark_cloud_piercing",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ohlc",
    "long": "prior down candle, gap-down open, close back above prior midpoint but below prior open (piercing)",
    "short": "prior up candle, gap-up open above prior high, close below prior midpoint but above prior open (dark cloud)",
    "desc": "two-candle partial-penetration reversal needing a gap then a close past the prior body midpoint",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I['open'][i]; c = I['close'][i]
    o1 = I['open'][i-1]; c1 = I['close'][i-1]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    if _nan(o, c, o1, c1, h1, l1):
        return None
    mid1 = (o1 + c1) / 2.0
    if c1 < o1 and o < l1 and c > mid1 and c < o1:
        return 'long'
    if c1 > o1 and o > h1 and c < mid1 and c > o1:
        return 'short'
    return None
