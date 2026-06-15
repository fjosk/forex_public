#!/usr/bin/env python3
"""close_location_momentum -- Close-Location-in-Range continuation: smoothed CLV crossing the upper/lower threshold signals sustained intrabar buying/selling pressure. Thresholds rescaled from the pseudocode 0.75/0.25 (0..1) to +0. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "close_location_momentum",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "15m-4h",
    "indicators": "Close-location-in-range SMA(3)",
    "long": "Smoothed close-location crosses up through +0.5 (upper-range continuation)",
    "short": "Smoothed close-location crosses down through -0.5 (lower-range continuation)",
    "desc": "Close-Location-in-Range continuation: smoothed CLV crossing the upper/lower threshold signals sustained intrabar buying/selling pressure. Thresholds rescaled from the pseudocode 0.75/0.25 (0..1) to +0",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    cl, cl1 = I["close_loc_sma"][i], I["close_loc_sma"][i-1]
    if _nan(cl, cl1):
        return None
    # NOTE: precomputed close_loc_sma is SMA(3) of CLV on the -1..+1 scale
    # ((c-l)-(h-c))/rng, NOT the 0..1 (c-l)/(h-l) the pseudocode assumed.
    # The pseudocode's 0.75/0.25 (0..1) thresholds re-map to +0.5/-0.5 here.
    if cl >= 0.5 and cl1 < 0.5:
        return "long"
    if cl <= -0.5 and cl1 > -0.5:
        return "short"
    return None
