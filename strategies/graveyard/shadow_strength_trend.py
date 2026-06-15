#!/usr/bin/env python3
"""shadow_strength_trend -- Candle shadow strength trend: a growing average lower wick (buyers rejecting lows) implies demand pressure; mirror for upper wick supply pressure.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "shadow_strength_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "lo_shadow_sma,up_shadow_sma",
    "long": "Average lower shadow (SMA of (min(o,c)-low),14) is rising while average upper shadow is not",
    "short": "Average upper shadow (SMA of (high-max(o,c)),14) is rising while average lower shadow is not",
    "desc": "Candle shadow strength trend: a growing average lower wick (buyers rejecting lows) implies demand pressure; mirror for upper wick supply pressure.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    lo = I['lo_shadow_sma'][i]; lo1 = I['lo_shadow_sma'][i-1]
    up = I['up_shadow_sma'][i]; up1 = I['up_shadow_sma'][i-1]
    if _nan(lo, lo1, up, up1):
        return None
    lo_up = lo > lo1
    up_up = up > up1
    if lo_up and not up_up:
        return 'long'
    if up_up and not lo_up:
        return 'short'
    return None
