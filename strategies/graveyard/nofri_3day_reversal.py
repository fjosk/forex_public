#!/usr/bin/env python3
"""nofri_3day_reversal -- Nofri congestion fade: inside a low-ADX range, two same-direction closes overextend the move and set up a snap-back reversal.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "nofri_3day_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "ADX(14), Close",
    "long": "In congestion (ADX<20), two consecutive down-closes signal a fade long",
    "short": "In congestion (ADX<20), two consecutive up-closes signal a fade short",
    "desc": "Nofri congestion fade: inside a low-ADX range, two same-direction closes overextend the move and set up a snap-back reversal.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    adx = I["adx"][i]
    c, c1, c2 = I["close"][i], I["close"][i-1], I["close"][i-2]
    if _nan(adx, c, c1, c2):
        return None
    ranging = adx < 20
    two_down = c < c1 and c1 < c2
    two_up = c > c1 and c1 > c2
    if ranging and two_down:
        return "long"
    if ranging and two_up:
        return "short"
    return None
