#!/usr/bin/env python3
"""tsi_signal_cross -- True Strength Index signal-line cross (double-smoothed momentum).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, _xdn, _xup, TREND_FLIP, ALL_CLASSES

META = {
    "id": "tsi_signal_cross",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "tsi,tsi_sig",
    "long": "TSI crosses above its 7-EMA signal line",
    "short": "TSI crosses below its signal line",
    "desc": "True Strength Index signal-line cross (double-smoothed momentum).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    t, s, t1, s1 = I["tsi"][i], I["tsi_sig"][i], I["tsi"][i-1], I["tsi_sig"][i-1]
    if _nan(t, s, t1, s1):
        return None
    if _xup(t, t1, s, s1):
        return "long"
    if _xdn(t, t1, s, s1):
        return "short"
    return None
