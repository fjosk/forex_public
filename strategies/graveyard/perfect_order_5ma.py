#!/usr/bin/env python3
"""perfect_order_5ma -- Five-MA perfect-order alignment confirmed by a rising ADX above 20. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "perfect_order_5ma",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma10,sma20,sma50,sma100,sma200,adx",
    "long": "Five SMAs in bullish perfect order (10>20>50>100>200) with ADX>20 and rising",
    "short": "Five SMAs in bearish perfect order (10<20<50<100<200) with ADX>20 and rising",
    "desc": "Five-MA perfect-order alignment confirmed by a rising ADX above 20",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    s10, s20, s50, s100, s200 = I["sma10"][i], I["sma20"][i], I["sma50"][i], I["sma100"][i], I["sma200"][i]
    adx, adx1 = I["adx"][i], I["adx"][i-1]
    if _nan(s10, s20, s50, s100, s200, adx, adx1):
        return None
    bull = s10 > s20 > s50 > s100 > s200
    bear = s10 < s20 < s50 < s100 < s200
    if bull and adx > 20 and adx > adx1:
        return "long"
    if bear and adx > 20 and adx > adx1:
        return "short"
    return None
