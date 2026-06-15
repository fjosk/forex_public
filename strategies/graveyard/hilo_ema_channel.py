#!/usr/bin/env python3
"""hilo_ema_channel -- Elder high/low EMA channel breakout on the first close outside the band. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "hilo_ema_channel",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close,ema_hi13,ema_lo13",
    "long": "Close breaks above the EMA(high,13) upper channel",
    "short": "Close breaks below the EMA(low,13) lower channel",
    "desc": "Elder high/low EMA channel breakout on the first close outside the band",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    hi, hi1 = I["ema_hi13"][i], I["ema_hi13"][i-1]
    lo, lo1 = I["ema_lo13"][i], I["ema_lo13"][i-1]
    if _nan(c, c1, hi, hi1, lo, lo1):
        return None
    if c > hi and c1 <= hi1:
        return "long"
    if c < lo and c1 >= lo1:
        return "short"
    return None
