#!/usr/bin/env python3
"""lag2_price_continuation -- Two-bar lagged price continuation (sign of a delayed one-bar return).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "lag2_price_continuation",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Close two bars ago was above the close three bars ago",
    "short": "Close two bars ago was below the close three bars ago",
    "desc": "Two-bar lagged price continuation (sign of a delayed one-bar return).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 3:
        return None
    c2, c3 = I["close"][i-2], I["close"][i-3]
    if _nan(c2, c3):
        return None
    if c2 > c3:
        return "long"
    if c2 < c3:
        return "short"
    return None
