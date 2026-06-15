#!/usr/bin/env python3
"""consec_down_close_fade -- Fade a three-bar close streak as short-term exhaustion.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "consec_down_close_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Three consecutive lower closes -> fade long",
    "short": "Three consecutive higher closes -> fade short",
    "desc": "Fade a three-bar close streak as short-term exhaustion.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 3:
        return None
    c, c1, c2, c3 = I["close"][i], I["close"][i-1], I["close"][i-2], I["close"][i-3]
    if _nan(c, c1, c2, c3):
        return None
    if c < c1 and c1 < c2 and c2 < c3:        # three lower closes in a row -> fade long
        return "long"
    if c > c1 and c1 > c2 and c2 > c3:        # three higher closes in a row -> fade short
        return "short"
    return None
