#!/usr/bin/env python3
"""ewo_wave -- Elliott Wave Oscillator zero-line cross signals the impulse-direction shift. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ewo_wave",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ewo",
    "long": "Elliott Wave Oscillator (SMA5-SMA35 of HL2) crosses above zero",
    "short": "Elliott Wave Oscillator (SMA5-SMA35 of HL2) crosses below zero",
    "desc": "Elliott Wave Oscillator zero-line cross signals the impulse-direction shift",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e, e1 = I["ewo"][i], I["ewo"][i-1]
    if _nan(e, e1):
        return None
    if e > 0 and e1 <= 0:
        return "long"
    if e < 0 and e1 >= 0:
        return "short"
    return None
