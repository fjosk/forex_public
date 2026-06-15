#!/usr/bin/env python3
"""settlement_reversal_bar -- Settlement-price reversal bar: range pushes with the EMA20 trend but the close settles against it, signaling exhaustion (mean-revert).. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "settlement_reversal_bar",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "candlestick",
    "tf": "1h-4h",
    "indicators": "EMA(20), OHLC",
    "long": "With-trend higher range (HH+HL) but close below prior close in an uptrend -> short",
    "short": "With-trend lower range (LL+LH) but close above prior close in a downtrend -> long",
    "desc": "Settlement-price reversal bar: range pushes with the EMA20 trend but the close settles against it, signaling exhaustion (mean-revert).",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    c, c1 = I["close"][i], I["close"][i-1]
    e1 = I["ema20"][i-1]
    if _nan(hi, hi1, lo, lo1, c, c1, e1):
        return None
    if hi > hi1 and lo > lo1 and c < c1 and c1 > e1:
        return "short"
    if lo < lo1 and hi < hi1 and c > c1 and c1 < e1:
        return "long"
    return None
