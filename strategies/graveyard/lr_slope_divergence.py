#!/usr/bin/env python3
"""lr_slope_divergence -- Linear-regression slope divergence: opposing 20-bar regression slopes of price vs RSI flag momentum divergence; fade the price slope.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "lr_slope_divergence",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "lr_slope_price,lr_slope_rsi",
    "long": "20-bar linear-regression slope of price is negative while slope of RSI is positive (bullish divergence)",
    "short": "20-bar linear-regression slope of price is positive while slope of RSI is negative (bearish divergence)",
    "desc": "Linear-regression slope divergence: opposing 20-bar regression slopes of price vs RSI flag momentum divergence; fade the price slope.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    sp = I['lr_slope_price'][i]; sr = I['lr_slope_rsi'][i]
    if _nan(sp, sr):
        return None
    if sp < 0 and sr > 0:
        return 'long'
    if sp > 0 and sr < 0:
        return 'short'
    return None
