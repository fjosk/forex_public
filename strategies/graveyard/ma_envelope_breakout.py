#!/usr/bin/env python3
"""ma_envelope_breakout -- Percentage envelope breakout around SMA20 (+/-3%) on first close outside the band. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "ma_envelope_breakout",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "sma20,close",
    "long": "Close breaks above +3% SMA20 envelope after being inside",
    "short": "Close breaks below -3% SMA20 envelope after being inside",
    "desc": "Percentage envelope breakout around SMA20 (+/-3%) on first close outside the band",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]
    s = I['sma20'][i]; s1 = I['sma20'][i-1]
    if _nan(c, c1, s, s1):
        return None
    up = s * 1.03; lo = s * 0.97
    if c > up and c1 <= s1 * 1.03:
        return 'long'
    if c < lo and c1 >= s1 * 0.97:
        return 'short'
    return None
