#!/usr/bin/env python3
"""willr_protrend_pullback -- Williams %R pro-trend deep-pullback continuation: add in the EMA50/EMA200 trend direction as %R rebounds from an extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "willr_protrend_pullback",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "Williams %R(14), EMA(50), EMA(200)",
    "long": "EMA50>EMA200 and %R turning up from <= -95 (deep-pullback add)",
    "short": "EMA50<EMA200 and %R turning down from >= -10 (deep-pullback add)",
    "desc": "Williams %R pro-trend deep-pullback continuation: add in the EMA50/EMA200 trend direction as %R rebounds from an extreme.",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    w, w1 = I["willr"][i], I["willr"][i-1]
    e50, e200 = I["ema50"][i], I["ema200"][i]
    if _nan(w, w1, e50, e200):
        return None
    trend_up = e50 > e200
    if trend_up and w1 <= -95 and w > w1:     # deep oversold pullback turning up in an uptrend
        return "long"
    if (not trend_up) and w1 >= -10 and w < w1:  # deep overbought pullback turning down in a downtrend
        return "short"
    return None
