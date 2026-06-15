#!/usr/bin/env python3
"""bookstaber_atr_breakout -- Bookstaber close-to-close ATR breakout: a single-bar move larger than 3 ATR signals a volatility expansion to ride.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "bookstaber_atr_breakout",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "Close, ATR(14)",
    "long": "Close-to-close move up exceeds 3x ATR",
    "short": "Close-to-close move down exceeds 3x ATR",
    "desc": "Bookstaber close-to-close ATR breakout: a single-bar move larger than 3 ATR signals a volatility expansion to ride.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, c1, a = I["close"][i], I["close"][i-1], I["atr"][i]
    if _nan(c, c1, a):
        return None
    K = 3.0
    if (c - c1) > K * a:
        return "long"
    if (c1 - c) > K * a:
        return "short"
    return None
