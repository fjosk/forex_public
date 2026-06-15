#!/usr/bin/env python3
"""round_number_first_cross -- First-cross round-number breakout: trade the first close through a price-magnitude round level the prior bar had not yet touched.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "round_number_first_cross",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "round_step,close,high,low",
    "long": "Close crosses up through the next round-number level for the first time (prior bar stayed below it)",
    "short": "Close crosses down through the round-number level for the first time (prior bar stayed above it)",
    "desc": "First-cross round-number breakout: trade the first close through a price-magnitude round level the prior bar had not yet touched.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    import math
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    h1, l1 = I["high"][i-1], I["low"][i-1]
    step = I["round_step"][i]
    if _nan(c, c1, h1, l1, step) or step <= 0:
        return None
    level = math.ceil(c1 / step) * step
    flr = math.floor(c1 / step) * step
    if c1 < level <= c and h1 < level:
        return "long"
    if c1 > flr >= c and l1 > flr:
        return "short"
    return None
