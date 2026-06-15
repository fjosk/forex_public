#!/usr/bin/env python3
"""macd_hist_slope_tick -- MACD-histogram bar-to-bar slope tick (momentum inflection).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_hist_slope_tick",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MACD(12,26,9) histogram",
    "long": "MACD histogram slope turns up (rises after a non-rising bar)",
    "short": "MACD histogram slope turns down (falls after a non-falling bar)",
    "desc": "MACD-histogram bar-to-bar slope tick (momentum inflection).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    hh, h1, h2 = I["macd_hist"][i], I["macd_hist"][i-1], I["macd_hist"][i-2]
    if _nan(hh, h1, h2):
        return None
    if hh > h1 and h1 <= h2:
        return "long"
    if hh < h1 and h1 >= h2:
        return "short"
    return None
