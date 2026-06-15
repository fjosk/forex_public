#!/usr/bin/env python3
"""macd_signal_line_cross -- Classic MACD line / signal-line crossover.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, _xdn, _xup, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_signal_line_cross",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "MACD(12,26,9)",
    "long": "MACD line crosses above its signal line",
    "short": "MACD line crosses below its signal line",
    "desc": "Classic MACD line / signal-line crossover.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    if _nan(m, s, m1, s1):
        return None
    if _xup(m, m1, s, s1):
        return "long"
    if _xdn(m, m1, s, s1):
        return "short"
    return None
