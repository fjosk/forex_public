#!/usr/bin/env python3
"""oops_gap_fade_pri -- Williams Oops: fade an opening gap once price trades back into the prior bar range.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_gap_fade_pri",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "open, high, low",
    "long": "Open below prior bar low then high re-enters it -> long",
    "short": "Open above prior bar high then low re-enters it -> short",
    "desc": "Williams Oops: fade an opening gap once price trades back into the prior bar range.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I["open"][i]
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    if _nan(o, hi, hi1, lo, lo1):
        return None
    if o < lo1 and hi >= lo1:                 # gapped below prior low then traded back up into it -> long
        return "long"
    if o > hi1 and lo <= hi1:                 # gapped above prior high then traded back down into it -> short
        return "short"
    return None
