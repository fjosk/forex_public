#!/usr/bin/env python3
"""ema_below_low_rsi_value -- Deep-value entry: price has run far enough that the EMA20 sits beyond the prior bar range while momentum is still soft, a mean-reversion snapback setup.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "ema_below_low_rsi_value",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "EMA(20), RSI(14), prior High/Low",
    "long": "EMA20 below the prior bar low with RSI<50 (price stretched below its mean)",
    "short": "EMA20 above the prior bar high with RSI>50",
    "desc": "Deep-value entry: price has run far enough that the EMA20 sits beyond the prior bar range while momentum is still soft, a mean-reversion snapback setup.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e, r = I["ema20"][i], I["rsi"][i]
    l1, h1 = I["low"][i-1], I["high"][i-1]
    if _nan(e, r, l1, h1):
        return None
    if e < l1 and r < 50:
        return "long"
    if e > h1 and r > 50:
        return "short"
    return None
