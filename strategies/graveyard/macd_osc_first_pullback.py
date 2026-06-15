#!/usr/bin/env python3
"""macd_osc_first_pullback -- Raschke first-cross pullback entry (momentum dip with price structure holding).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "macd_osc_first_pullback",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MACD(12,26,9), high, low",
    "long": "MACD ticks back down through signal while price holds a higher low (first pullback in an up-leg)",
    "short": "MACD ticks back up through signal while price holds a lower high (first pullback in a down-leg)",
    "desc": "Raschke first-cross pullback entry (momentum dip with price structure holding).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o, s, o1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    if _nan(o, s, o1, s1, lo, lo1, hi, hi1):
        return None
    if o1 > s1 and o <= s and lo > lo1:
        return "long"
    if o1 < s1 and o >= s and hi < hi1:
        return "short"
    return None
