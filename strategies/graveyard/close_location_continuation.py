#!/usr/bin/env python3
"""close_location_continuation -- Close Location Value continuation: where the close sits inside the bar range signals intrabar buying/selling pressure.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "close_location_continuation",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "15m-4h",
    "indicators": "High, Low, Close",
    "long": "Close lands in the upper 35% of the bar range (CLV>=0.65)",
    "short": "Close lands in the lower 35% of the bar range (CLV<=0.35)",
    "desc": "Close Location Value continuation: where the close sits inside the bar range signals intrabar buying/selling pressure.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 0:
        return None
    h, l, c = I["high"][i], I["low"][i], I["close"][i]
    if _nan(h, l, c):
        return None
    rng = h - l
    clv = (c - l) / rng if rng > 0 else 0.5
    if clv >= 0.65:
        return "long"
    if clv <= 0.35:
        return "short"
    return None
