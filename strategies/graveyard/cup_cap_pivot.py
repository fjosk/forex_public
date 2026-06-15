#!/usr/bin/env python3
"""cup_cap_pivot -- Colby-Meyers cup/cap 3-bar pivot reversal, EMA20-filtered.. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "cup_cap_pivot",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "pattern",
    "tf": "1h-4h",
    "indicators": "EMA20, raw OHLC",
    "long": "Cup 3-bar pivot (prior bar low is local min) and close breaks above it while prior close was below EMA20",
    "short": "Cap 3-bar pivot (prior bar high is local max) and close breaks below it while prior close was above EMA20",
    "desc": "Colby-Meyers cup/cap 3-bar pivot reversal, EMA20-filtered.",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    h, h1, h2 = I["high"][i], I["high"][i-1], I["high"][i-2]
    l, l1, l2 = I["low"][i], I["low"][i-1], I["low"][i-2]
    c, c1 = I["close"][i], I["close"][i-1]
    e1 = I["ema20"][i-1]
    if _nan(h, h1, h2, l, l1, l2, c, c1, e1):
        return None
    cap = h1 > h2 and h1 > h
    cup = l1 < l2 and l1 < l
    if cup and c > h1 and c1 < e1:
        return "long"
    if cap and c < l1 and c1 > e1:
        return "short"
    return None
