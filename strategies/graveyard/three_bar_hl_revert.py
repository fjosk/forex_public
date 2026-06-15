#!/usr/bin/env python3
"""three_bar_hl_revert -- Three-bar high/low limit reversion: in a trend, buy dips to the short-term average low and sell rallies to the average high.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "three_bar_hl_revert",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "high,low,ema50,sma3_low,sma3_high",
    "long": "Uptrend (close>EMA50) and low tags the 3-bar average low (SMA(low,3))",
    "short": "Downtrend (close<EMA50) and high tags the 3-bar average high (SMA(high,3))",
    "desc": "Three-bar high/low limit reversion: in a trend, buy dips to the short-term average low and sell rallies to the average high.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 3:
        return None
    c = I['close'][i]; e50 = I['ema50'][i]
    lo = I['low'][i]; hi = I['high'][i]
    s3l = I['sma3_low'][i]; s3h = I['sma3_high'][i]
    if _nan(c, e50, lo, hi, s3l, s3h):
        return None
    trend_up = c > e50
    trend_dn = c < e50
    if trend_up and lo <= s3l:
        return 'long'
    if trend_dn and hi >= s3h:
        return 'short'
    return None
