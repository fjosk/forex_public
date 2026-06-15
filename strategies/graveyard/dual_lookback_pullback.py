#!/usr/bin/env python3
"""dual_lookback_pullback -- Dual-lookback: trade the short-term counter-move inside the longer trend.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "dual_lookback_pullback",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Up over 30 bars but down over 9 bars -> buy pullback",
    "short": "Down over 30 bars but up over 9 bars -> sell bounce",
    "desc": "Dual-lookback: trade the short-term counter-move inside the longer trend.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 30:
        return None
    c, c9, c30 = I["close"][i], I["close"][i-9], I["close"][i-30]
    if _nan(c, c9, c30):
        return None
    if c > c30 and c < c9:                    # longer-term up, short-term dip -> buy the pullback
        return "long"
    if c < c30 and c > c9:                    # longer-term down, short-term pop -> sell the bounce
        return "short"
    return None
