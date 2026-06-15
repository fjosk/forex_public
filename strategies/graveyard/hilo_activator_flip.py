#!/usr/bin/env python3
"""hilo_activator_flip -- HiLo Activator: long when close breaks above the moving average of highs, short when it breaks below the moving average of lows.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "hilo_activator_flip",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "sma_high21,sma_low21,close",
    "long": "Close crosses above the 21-bar SMA of highs",
    "short": "Close crosses below the 21-bar SMA of lows",
    "desc": "HiLo Activator: long when close breaks above the moving average of highs, short when it breaks below the moving average of lows.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    shi, shi1 = I["sma_high21"][i], I["sma_high21"][i-1]
    slo, slo1 = I["sma_low21"][i], I["sma_low21"][i-1]
    if _nan(c, c1, shi, shi1, slo, slo1):
        return None
    if c > shi and c1 <= shi1:
        return "long"
    if c < slo and c1 >= slo1:
        return "short"
    return None
