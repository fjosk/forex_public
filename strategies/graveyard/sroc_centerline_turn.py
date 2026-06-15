#!/usr/bin/env python3
"""sroc_centerline_turn -- Smoothed Rate of Change centerline turn: buy an upturn while negative, sell a downturn while positive.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "sroc_centerline_turn",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "sroc",
    "long": "S-ROC below zero and turning up (rising off a trough)",
    "short": "S-ROC above zero and turning down (rolling off a peak)",
    "desc": "Smoothed Rate of Change centerline turn: buy an upturn while negative, sell a downturn while positive.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    s, s1 = I["sroc"][i], I["sroc"][i-1]
    if _nan(s, s1):
        return None
    if s1 < 0 and s > s1:
        return "long"
    if s1 > 0 and s < s1:
        return "short"
    return None
