#!/usr/bin/env python3
"""outside_reversal_rsi -- Outside-reversal bar combined with an RSI extreme (Cambridge hook): engulfing range plus stretched momentum.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "outside_reversal_rsi",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "OHLC, RSI(14)",
    "long": "Outside bar that closes UP while RSI<40 (oversold) -- bullish Cambridge hook",
    "short": "Outside bar that closes DOWN while RSI>60 (overbought) -- bearish Cambridge hook",
    "desc": "Outside-reversal bar combined with an RSI extreme (Cambridge hook): engulfing range plus stretched momentum.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    h0, h1 = I["high"][i], I["high"][i-1]
    l0, l1 = I["low"][i], I["low"][i-1]
    c0, c1 = I["close"][i], I["close"][i-1]
    r = I["rsi"][i]
    if _nan(h0, h1, l0, l1, c0, c1, r):
        return None
    outside = h0 > h1 and l0 < l1
    if outside and c0 < c1 and r > 60:
        return "short"
    if outside and c0 > c1 and r > 40 - 1e-9 and r < 40:
        return "long"
    return None
