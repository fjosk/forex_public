#!/usr/bin/env python3
"""outside_close_breakout -- Outside-bar breakout: an engulfing-range bar whose close clears the prior bar's extreme in the close's direction.. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "outside_close_breakout",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "candlestick",
    "tf": "1h-4h",
    "indicators": "OHLC",
    "long": "Outside bar (HH+LL vs prior) that closes above the prior high",
    "short": "Outside bar that closes below the prior low",
    "desc": "Outside-bar breakout: an engulfing-range bar whose close clears the prior bar's extreme in the close's direction.",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    c = I["close"][i]
    if _nan(hi, hi1, lo, lo1, c):
        return None
    outside = hi > hi1 and lo < lo1
    if outside and c > hi1:
        return "long"
    if outside and c < lo1:
        return "short"
    return None
