#!/usr/bin/env python3
"""range_compression_breakout -- Range-compression breakout: a contracted recent range relative to the longer range primes a trend-aligned Donchian breakout.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "range_compression_breakout",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "SMA(50), Donchian channel (dc_up/dc_lo), 5-bar range (rng5), 50-bar range (rng50)",
    "long": "5-bar range squeezed to <=60% of the 50-bar range, price above SMA50, and high takes out the prior Donchian upper",
    "short": "5-bar range squeezed to <=60% of the 50-bar range, price below SMA50, and low takes out the prior Donchian lower",
    "desc": "Range-compression breakout: a contracted recent range relative to the longer range primes a trend-aligned Donchian breakout.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    r5, r50 = I["rng5"][i], I["rng50"][i]
    c, s = I["close"][i], I["sma50"][i]
    h, l = I["high"][i], I["low"][i]
    du1, dl1 = I["dc_up"][i-1], I["dc_lo"][i-1]
    if _nan(r5, r50, c, s, h, l, du1, dl1):
        return None
    if not (r5 <= 0.60 * r50):
        return None
    if c > s and h >= du1:
        return "long"
    if c < s and l <= dl1:
        return "short"
    return None
