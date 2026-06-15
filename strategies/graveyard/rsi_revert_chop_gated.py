#!/usr/bin/env python3
"""rsi_revert_chop_gated -- RSI band re-cross mean-reversion, gated to a non-trending (ADX<25) regime so it only fires in chop.. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_revert_chop_gated",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h-4h",
    "indicators": "RSI(14), ADX(14)",
    "long": "ADX<25 and RSI re-crosses up through 25",
    "short": "ADX<25 and RSI re-crosses down through 75",
    "desc": "RSI band re-cross mean-reversion, gated to a non-trending (ADX<25) regime so it only fires in chop.",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    r, r1, adx = I["rsi"][i], I["rsi"][i-1], I["adx"][i]
    if _nan(r, r1, adx):
        return None
    if adx >= 25:                             # only fade in a non-trending regime
        return None
    if r1 <= 25 and r > 25:                    # RSI re-crosses up through 25
        return "long"
    if r1 >= 75 and r < 75:                    # RSI re-crosses down through 75
        return "short"
    return None
