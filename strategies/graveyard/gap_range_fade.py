#!/usr/bin/env python3
"""gap_range_fade -- Prior-day range gap fade: take the gap back into the range once momentum stalls.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "gap_range_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "day_open, prev_dhh, prev_dll, high, low",
    "long": "Day opens below prior-day low and bar holds (low>=prev low) -> long",
    "short": "Day opens above prior-day high and bar caps (high<=prev high) -> short",
    "desc": "Prior-day range gap fade: take the gap back into the range once momentum stalls.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    do = I["day_open"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    if _nan(do, pdll, pdhh, lo, lo1, hi, hi1):
        return None
    if do < pdll and lo >= lo1:               # gapped below prior-day range, holding (not making new low) -> long
        return "long"
    if do > pdhh and hi <= hi1:               # gapped above prior-day range, capped (not making new high) -> short
        return "short"
    return None
