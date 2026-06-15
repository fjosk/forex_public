#!/usr/bin/env python3
"""fader_false_break -- The Fader: fade a buffered false break of the prior-day range in a non-trending regime.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "fader_false_break",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "ADX(14), prev_dhh, prev_dll, low, high, close",
    "long": "ADX<35, low breaks prior-day low by buffer then close back above it -> long",
    "short": "ADX<35, high breaks prior-day high by buffer then close back below it -> short",
    "desc": "The Fader: fade a buffered false break of the prior-day range in a non-trending regime.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    adx = I["adx"][i]
    c = I["close"][i]
    lo, hi = I["low"][i], I["high"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    if _nan(adx, c, lo, hi, pdll, pdhh):
        return None
    not_strong = adx < 35
    buf = 0.0015 * c
    if not_strong and lo < pdll - buf and c > pdll:     # poked below prior-day low then closed back inside
        return "long"
    if not_strong and hi > pdhh + buf and c < pdhh:     # poked above prior-day high then closed back inside
        return "short"
    return None
