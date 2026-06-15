#!/usr/bin/env python3
"""belt_hold_flip -- belt-hold open-on-extreme reversal: a no-wick open side bar closing back into trend against ema20 context. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "belt_hold_flip",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ema20,ohlc",
    "long": "open shaved on low (open-low<=5% range) + close up while prior bar below ema20",
    "short": "open shaved on high (high-open<=5% range) + close down while prior bar above ema20",
    "desc": "belt-hold open-on-extreme reversal: a no-wick open side bar closing back into trend against ema20 context",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]; c = I['close'][i]
    c1 = I['close'][i-1]; e1 = I['ema20'][i-1]
    if _nan(o, h, l, c, c1, e1):
        return None
    rng = h - l
    if rng <= 0:
        return None
    k = 0.05
    if (o - l) <= k * rng and c > o and c1 < e1:
        return 'long'
    if (h - o) <= k * rng and c < o and c1 > e1:
        return 'short'
    return None
