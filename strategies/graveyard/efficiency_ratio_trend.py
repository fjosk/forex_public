#!/usr/bin/env python3
"""efficiency_ratio_trend -- Trend entry gated by a high Kaufman efficiency ratio so only directional (non-choppy) moves trade. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "efficiency_ratio_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "er10,ema20,close",
    "long": "Kaufman efficiency ratio >=0.6 with EMA20 rising and close above it",
    "short": "Kaufman efficiency ratio >=0.6 with EMA20 falling and close below it",
    "desc": "Trend entry gated by a high Kaufman efficiency ratio so only directional (non-choppy) moves trade",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    er, e, e1, c = I["er10"][i], I["ema20"][i], I["ema20"][i-1], I["close"][i]
    if _nan(er, e, e1, c):
        return None
    if er >= 0.6 and e > e1 and c > e:
        return "long"
    if er >= 0.6 and e < e1 and c < e:
        return "short"
    return None
