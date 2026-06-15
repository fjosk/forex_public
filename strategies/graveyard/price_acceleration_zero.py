#!/usr/bin/env python3
"""price_acceleration_zero -- Price acceleration zero-cross: the second difference of price (change in 10-bar momentum) flipping sign.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "price_acceleration_zero",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "accel",
    "long": "Price acceleration (2nd difference of 10-bar momentum) crosses above zero",
    "short": "Price acceleration crosses below zero",
    "desc": "Price acceleration zero-cross: the second difference of price (change in 10-bar momentum) flipping sign.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    a, a1 = I["accel"][i], I["accel"][i-1]
    if _nan(a, a1):
        return None
    if a > 0 and a1 <= 0:
        return "long"
    if a < 0 and a1 >= 0:
        return "short"
    return None
