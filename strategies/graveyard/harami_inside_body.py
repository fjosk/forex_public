#!/usr/bin/env python3
"""harami_inside_body -- body-inside-prior-large-body contraction signalling momentum stall, filtered by ema20 trend context. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "harami_inside_body",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ema20,ohlc",
    "long": "current body inside prior large down body (>1.5x bar i-2 body) while prior bar below ema20 (bull harami in downtrend)",
    "short": "current body inside prior large up body while prior bar above ema20 (bear harami in uptrend)",
    "desc": "body-inside-prior-large-body contraction signalling momentum stall, filtered by ema20 trend context",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    o = I['open'][i]; c = I['close'][i]
    o1 = I['open'][i-1]; c1 = I['close'][i-1]
    o2 = I['open'][i-2]; c2 = I['close'][i-2]
    e1 = I['ema20'][i-1]
    if _nan(o, c, o1, c1, o2, c2, e1):
        return None
    body1 = abs(c1 - o1)
    inside = (max(o, c) <= max(o1, c1)) and (min(o, c) >= min(o1, c1))
    big1 = body1 > 1.5 * abs(c2 - o2)
    if inside and big1 and c1 < o1 and c1 < e1:
        return 'long'
    if inside and big1 and c1 > o1 and c1 > e1:
        return 'short'
    return None
