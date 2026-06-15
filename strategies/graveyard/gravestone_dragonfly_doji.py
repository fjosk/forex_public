#!/usr/bin/env python3
"""gravestone_dragonfly_doji -- one-sided-wick doji extreme-rejection reversal filtered by ema20 trend context. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "gravestone_dragonfly_doji",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "ema20,ohlc",
    "long": "dragonfly doji (tiny body at the top, long lower wick) while close below ema20 -> long",
    "short": "gravestone doji (tiny body at the bottom, long upper wick) while close above ema20 -> short",
    "desc": "one-sided-wick doji extreme-rejection reversal filtered by ema20 trend context",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 0:
        return None
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]; c = I['close'][i]
    e = I['ema20'][i]
    if _nan(o, h, l, c, e):
        return None
    rng = h - l
    if rng <= 0:
        return None
    body = abs(c - o)
    is_doji = body <= 0.05 * rng
    if not is_doji:
        return None
    upper = h - max(o, c)
    lower = min(o, c) - l
    if lower <= 0.1 * rng and upper >= 0.6 * rng and c > e:
        return 'short'
    if upper <= 0.1 * rng and lower >= 0.6 * rng and c < e:
        return 'long'
    return None
