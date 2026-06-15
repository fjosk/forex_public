#!/usr/bin/env python3
"""macd_signal_cross_countertrend_gated -- MACD signal-line cross gated by the zero side (counter-trend mean-reversion).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, _xdn, _xup, REVERT, ALL_CLASSES

META = {
    "id": "macd_signal_cross_countertrend_gated",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MACD(12,26,9)",
    "long": "MACD crosses above signal while still below zero",
    "short": "MACD crosses below signal while still above zero",
    "desc": "MACD signal-line cross gated by the zero side (counter-trend mean-reversion).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    if _nan(m, s, m1, s1):
        return None
    if _xup(m, m1, s, s1) and m < 0:
        return "long"
    if _xdn(m, m1, s, s1) and m > 0:
        return "short"
    return None
