#!/usr/bin/env python3
"""momentum_break_macdhist_chop -- Range-regime breakout: only takes Donchian breaks out of a high-choppiness coil, confirmed by MACD-histogram sign.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "momentum_break_macdhist_chop",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "Choppiness Index, Donchian(up/lo), MACD-hist",
    "long": "Choppy regime (CHOP>55) and close breaks above prior Donchian upper with MACD-hist > 0",
    "short": "Choppy regime and close breaks below prior Donchian lower with MACD-hist < 0",
    "desc": "Range-regime breakout: only takes Donchian breaks out of a high-choppiness coil, confirmed by MACD-histogram sign.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    chop, c, du, dl, mh = I["chop"][i], I["close"][i], I["dc_up"][i-1], I["dc_lo"][i-1], I["macd_hist"][i]
    if _nan(chop, c, du, dl, mh):
        return None
    flat = chop > 55
    if flat and c > du and mh > 0:
        return "long"
    if flat and c < dl and mh < 0:
        return "short"
    return None
