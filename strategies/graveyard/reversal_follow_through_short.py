#!/usr/bin/env python3
"""reversal_follow_through_short -- Failed-reversal fade: a sweep beyond the prior extreme that closes against the sweep direction signals exhaustion.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "reversal_follow_through_short",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "OHLC",
    "long": "Bar makes a higher high but closes lower than prior bar -- fade the failed up-move",
    "short": "Bar makes a lower low but closes higher than prior bar -- fade the failed down-move",
    "desc": "Failed-reversal fade: a sweep beyond the prior extreme that closes against the sweep direction signals exhaustion.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    h0, h1 = I["high"][i], I["high"][i-1]
    l0, l1 = I["low"][i], I["low"][i-1]
    c0, c1 = I["close"][i], I["close"][i-1]
    if _nan(h0, h1, l0, l1, c0, c1):
        return None
    if l0 < l1 and c0 > c1:
        return "short"
    if h0 > h1 and c0 < c1:
        return "long"
    return None
