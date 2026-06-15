#!/usr/bin/env python3
"""dual_ma_neutral -- Dual-MA band with neutral middle state; signal only on transition into above/below both EMAs. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "dual_ma_neutral",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "close,ema20,ema50",
    "long": "Close newly above both EMA20 and EMA50",
    "short": "Close newly below both EMA20 and EMA50",
    "desc": "Dual-MA band with neutral middle state; signal only on transition into above/below both EMAs",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]
    e20 = I['ema20'][i]; e20p = I['ema20'][i-1]
    e50 = I['ema50'][i]; e50p = I['ema50'][i-1]
    if _nan(c, c1, e20, e20p, e50, e50p):
        return None
    above = c > e20 and c > e50
    below = c < e20 and c < e50
    above_prev = c1 > e20p and c1 > e50p
    below_prev = c1 < e20p and c1 < e50p
    if above and not above_prev:
        return 'long'
    if below and not below_prev:
        return 'short'
    return None
