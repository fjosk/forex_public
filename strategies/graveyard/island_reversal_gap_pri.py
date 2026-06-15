#!/usr/bin/env python3
"""island_reversal_gap_pri -- Two-sided island reversal: a one-bar island isolated by gaps on both sides marks a sharp turn.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "island_reversal_gap_pri",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "High, Low",
    "long": "Bar i-1 gapped DOWN away from i-2 (island bottom) and this bar gaps UP off it -- reversal up",
    "short": "Bar i-1 gapped UP away from i-2 (island top) and this bar gaps DOWN off it -- reversal down",
    "desc": "Two-sided island reversal: a one-bar island isolated by gaps on both sides marks a sharp turn.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    h0, l0 = I["high"][i], I["low"][i]
    h1, l1 = I["high"][i-1], I["low"][i-1]
    h2, l2 = I["high"][i-2], I["low"][i-2]
    if _nan(h0, l0, h1, l1, h2, l2):
        return None
    gap_up_in = l1 > h2
    gap_dn_out = h0 < l1
    gap_dn_in = h1 < l2
    gap_up_out = l0 > h1
    if gap_up_in and gap_dn_out:
        return "short"
    if gap_dn_in and gap_up_out:
        return "long"
    return None
