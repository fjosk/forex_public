#!/usr/bin/env python3
"""asi_swing_breakout -- Wilder Accumulated Swing Index breaking its last swing pivot confirms a price breakout. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "asi_swing_breakout",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "asi,asi_hsp,asi_lsp",
    "long": "Accumulated Swing Index breaks above the prior ASI high swing pivot",
    "short": "Accumulated Swing Index breaks below the prior ASI low swing pivot",
    "desc": "Wilder Accumulated Swing Index breaking its last swing pivot confirms a price breakout",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    a, a1 = I["asi"][i], I["asi"][i-1]
    hsp1, lsp1 = I["asi_hsp"][i-1], I["asi_lsp"][i-1]
    if _nan(a, a1, hsp1, lsp1):
        return None
    if a > hsp1 and a1 <= hsp1:
        return "long"
    if a < lsp1 and a1 >= lsp1:
        return "short"
    return None
