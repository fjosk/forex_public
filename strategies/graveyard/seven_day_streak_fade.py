#!/usr/bin/env python3
"""seven_day_streak_fade -- Body-streak exhaustion: fade after seven same-direction candles.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "seven_day_streak_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "open, close",
    "long": "Seven consecutive down-body candles -> fade long",
    "short": "Seven consecutive up-body candles -> fade short",
    "desc": "Body-streak exhaustion: fade after seven same-direction candles.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 6:
        return None
    os = I["open"][i-6:i+1]
    cs = I["close"][i-6:i+1]
    if len(os) < 7 or len(cs) < 7:
        return None
    if _nan(*os, *cs):
        return None
    if all(cs[j] < os[j] for j in range(7)):     # seven straight down (red body) candles -> fade long
        return "long"
    if all(cs[j] > os[j] for j in range(7)):     # seven straight up (green body) candles -> fade short
        return "short"
    return None
