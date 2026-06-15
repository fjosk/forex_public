#!/usr/bin/env python3
"""breakout_retest_reclaim -- Donchian breakout followed by a retest-and-hold reclaim within last 6 bars. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "breakout_retest_reclaim",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,dc_up,dc_lo",
    "long": "Recent Donchian-up break, retest of band, then bullish reclaim close",
    "short": "Recent Donchian-low break, retest of band, then bearish reclaim close",
    "desc": "Donchian breakout followed by a retest-and-hold reclaim within last 6 bars",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 7:
        return None
    o = I['open'][i]; c = I['close'][i]
    hi = I['high'][i]; lo = I['low'][i]
    dcu = I['dc_up'][i]; dcl = I['dc_lo'][i]
    if _nan(o, c, hi, lo, dcu, dcl):
        return None
    broke_up = False
    for j in range(i-6, i):
        cj = I['close'][j]; dcuj = I['dc_up'][j-1]
        if not _nan(cj, dcuj) and cj > dcuj:
            broke_up = True
            break
    retest = lo <= dcu * 1.002
    hold = c > dcu and c > o
    if broke_up and retest and hold:
        return 'long'
    broke_dn = False
    for j in range(i-6, i):
        cj = I['close'][j]; dclj = I['dc_lo'][j-1]
        if not _nan(cj, dclj) and cj < dclj:
            broke_dn = True
            break
    retest_d = hi >= dcl * 0.998
    hold_d = c < dcl and c < o
    if broke_dn and retest_d and hold_d:
        return 'short'
    return None
