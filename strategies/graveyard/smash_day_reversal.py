#!/usr/bin/env python3
"""smash_day_reversal -- Smash Day reversal: a naked-close exhaustion bar reversed by a break of the prior bar extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "smash_day_reversal",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "price_action",
    "tf": "1h-4h",
    "indicators": "high, low, close",
    "long": "Prior close below 2-bars-ago low, now high exceeds prior high -> long",
    "short": "Prior close above 2-bars-ago high, now low breaks prior low -> short",
    "desc": "Smash Day reversal: a naked-close exhaustion bar reversed by a break of the prior bar extreme.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    c1 = I["close"][i-1]
    lo2, lo1, lo = I["low"][i-2], I["low"][i-1], I["low"][i]
    hi2, hi1, hi = I["high"][i-2], I["high"][i-1], I["high"][i]
    if _nan(c1, lo2, lo1, lo, hi2, hi1, hi):
        return None
    if c1 < lo2 and hi > hi1:                 # prior bar smashed below the bar before it, now breaking back up -> long
        return "long"
    if c1 > hi2 and lo < lo1:                 # prior bar smashed above the bar before it, now breaking back down -> short
        return "short"
    return None
