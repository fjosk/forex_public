#!/usr/bin/env python3
"""pivot_bias_continuation -- Pivot-point bias continuation: take the PP-side breakout toward R1/S1 with EMA20 trend agreement.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "pivot_bias_continuation",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h (UTC-day)",
    "indicators": "Pivot point P/R1/S1, EMA20, close",
    "long": "Close crosses up through pivot P, above EMA20, headroom below R1",
    "short": "Close crosses down through pivot P, below EMA20, room above S1",
    "desc": "Pivot-point bias continuation: take the PP-side breakout toward R1/S1 with EMA20 trend agreement.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    p, r1, s1 = I['piv_p'][i], I['piv_r1'][i], I['piv_s1'][i]
    c, c1, e20 = I['close'][i], I['close'][i-1], I['ema20'][i]
    if _nan(p, r1, s1, c, c1, e20):
        return None
    if c1 <= p and c > p and c > e20 and c < r1:
        return 'long'
    if c1 >= p and c < p and c < e20 and c > s1:
        return 'short'
    return None
