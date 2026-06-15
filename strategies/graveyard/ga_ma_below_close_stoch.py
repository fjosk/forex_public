#!/usr/bin/env python3
"""ga_ma_below_close_stoch -- GA-evolved chromosome: MA position vs prior close confirmed by stochastic regime, fired only on the bar the condition first becomes true.. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "ga_ma_below_close_stoch",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "SMA(20), Stochastic %K, Close",
    "long": "SMA20 below prior close and %K>50, freshly true this bar",
    "short": "SMA20 above prior close and %K<50, freshly true this bar",
    "desc": "GA-evolved chromosome: MA position vs prior close confirmed by stochastic regime, fired only on the bar the condition first becomes true.",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    m, m1 = I["sma20"][i], I["sma20"][i-1]
    c1, c2 = I["close"][i-1], I["close"][i-2]
    k, k1 = I["stoch_k"][i], I["stoch_k"][i-1]
    if _nan(m, m1, c1, c2, k, k1):
        return None
    long_now = m < c1 and k > 50
    long_prev = m1 < c2 and k1 > 50
    short_now = m > c1 and k < 50
    short_prev = m1 > c2 and k1 < 50
    if long_now and not long_prev:
        return "long"
    if short_now and not short_prev:
        return "short"
    return None
