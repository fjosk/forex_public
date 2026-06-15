#!/usr/bin/env python3
"""elder_ray_triple_screen -- Elder Triple Screen (Elder-Ray Screen-2 variant): HTF trend bias + Elder-Ray power turning from its extreme + prior-bar break trigger.. tier2 (book-extracted from sister-lab catalog_books).

book:multi-timeframe. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "elder_ray_triple_screen",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "HTF EMA20/50 bias, Elder-Ray bull/bear power, close, prior high/low",
    "long": "HTF bias up, Bear Power negative but rising, close breaks prior high",
    "short": "HTF bias down, Bull Power positive but falling, close breaks prior low",
    "desc": "Elder Triple Screen (Elder-Ray Screen-2 variant): HTF trend bias + Elder-Ray power turning from its extreme + prior-bar break trigger.",
    "source": "book:multi-timeframe",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    bias = htf['bias'][i]
    bep, bep1 = I['bear_power'][i], I['bear_power'][i-1]
    bup, bup1 = I['bull_power'][i], I['bull_power'][i-1]
    c, ph, pl = I['close'][i], I['high'][i-1], I['low'][i-1]
    if _nan(bias, bep, bep1, bup, bup1, c, ph, pl):
        return None
    if bias > 0 and bep < 0 and bep > bep1 and c > ph:
        return 'long'
    if bias < 0 and bup > 0 and bup < bup1 and c < pl:
        return 'short'
    return None
