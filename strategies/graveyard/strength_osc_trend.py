#!/usr/bin/env python3
"""strength_osc_trend -- Chande/Kroll Strength Oscillator: ratio of averaged net price move to averaged range; a threshold cross signals directional strength.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "strength_osc_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "Strength Oscillator (net-move SMA / range SMA, 14)",
    "long": "Strength oscillator crosses above +0.30",
    "short": "Strength oscillator crosses below -0.30",
    "desc": "Chande/Kroll Strength Oscillator: ratio of averaged net price move to averaged range; a threshold cross signals directional strength.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    thr = 0.30
    s, s1 = I["strength_osc"][i], I["strength_osc"][i-1]
    if _nan(s, s1):
        return None
    if s > thr and s1 <= thr:
        return "long"
    if s < -thr and s1 >= -thr:
        return "short"
    return None
