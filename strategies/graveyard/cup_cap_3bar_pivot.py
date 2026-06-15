#!/usr/bin/env python3
"""cup_cap_3bar_pivot -- Cup-and-cap 3-bar swing pivot countertrend: trade the failure of the prevailing trend at a local pivot.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "cup_cap_3bar_pivot",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "OHLC, EMA(50)",
    "long": "In a downtrend (close<EMA50) a 3-bar cap pivot forms and this close breaks back above the pivot high",
    "short": "In an uptrend (close>EMA50) a 3-bar cup pivot forms and this close breaks back below the pivot low",
    "desc": "Cup-and-cap 3-bar swing pivot countertrend: trade the failure of the prevailing trend at a local pivot.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    c, e50 = I["close"][i], I["ema50"][i]
    h0, h1, h2 = I["high"][i], I["high"][i-1], I["high"][i-2]
    l0, l1, l2 = I["low"][i], I["low"][i-1], I["low"][i-2]
    if _nan(c, e50, h0, h1, h2, l0, l1, l2):
        return None
    cap = h1 > h2 and h1 > h0
    cup = l1 < l2 and l1 < l0
    if c < e50 and cap and c > h1:
        return "long"
    if c > e50 and cup and c < l1:
        return "short"
    return None
