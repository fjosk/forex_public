#!/usr/bin/env python3
"""forecast_oscillator_zero -- Forecast Oscillator zero-cross: smoothed percent deviation of close from its 3-bar time-series-forecast value.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "forecast_oscillator_zero",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "fosc",
    "long": "Forecast Oscillator (%F) crosses above zero (price above its regression forecast)",
    "short": "Forecast Oscillator crosses below zero",
    "desc": "Forecast Oscillator zero-cross: smoothed percent deviation of close from its 3-bar time-series-forecast value.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    f, f1 = I["fosc"][i], I["fosc"][i-1]
    if _nan(f, f1):
        return None
    if f > 0 and f1 <= 0:
        return "long"
    if f < 0 and f1 >= 0:
        return "short"
    return None
