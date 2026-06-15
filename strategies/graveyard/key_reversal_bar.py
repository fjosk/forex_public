#!/usr/bin/env python3
"""key_reversal_bar -- Key reversal bar: a new extreme that closes back through the prior close, taken counter to the prior EMA20 trend (mean-revert).. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "key_reversal_bar",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "candlestick",
    "tf": "1h-4h",
    "indicators": "EMA(20), OHLC",
    "long": "New lower low but close above prior close while prior close was below EMA20",
    "short": "New higher high but close below prior close while prior close was above EMA20",
    "desc": "Key reversal bar: a new extreme that closes back through the prior close, taken counter to the prior EMA20 trend (mean-revert).",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    c, c1 = I["close"][i], I["close"][i-1]
    e1 = I["ema20"][i-1]
    if _nan(lo, lo1, hi, hi1, c, c1, e1):
        return None
    if lo < lo1 and c > c1 and c1 < e1:
        return "long"
    if hi > hi1 and c < c1 and c1 > e1:
        return "short"
    return None
