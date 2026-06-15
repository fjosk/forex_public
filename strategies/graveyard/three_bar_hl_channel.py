#!/usr/bin/env python3
"""three_bar_hl_channel -- Williams 3-bar high/low MA channel: buy pullbacks to the low MA in an uptrend, mirror in downtrend. tier2 (book-extracted from sister-lab catalog_books).

book:trend. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "three_bar_hl_channel",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema50,high,low,mah3,mal3",
    "long": "EMA50 rising and low pulls back to touch the 3-bar low MA",
    "short": "EMA50 falling and high pulls back to touch the 3-bar high MA",
    "desc": "Williams 3-bar high/low MA channel: buy pullbacks to the low MA in an uptrend, mirror in downtrend",
    "source": "book:trend",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e, e1 = I["ema50"][i], I["ema50"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    mal, mal1 = I["mal3"][i], I["mal3"][i-1]
    mah, mah1 = I["mah3"][i], I["mah3"][i-1]
    if _nan(e, e1, lo, lo1, hi, hi1, mal, mal1, mah, mah1):
        return None
    up = e > e1
    dn = e < e1
    if up and lo <= mal and lo1 > mal1:
        return "long"
    if dn and hi >= mah and hi1 < mah1:
        return "short"
    return None
