#!/usr/bin/env python3
"""consecutive_record_exhaustion -- Consecutive new-record exhaustion reversal: a long unbroken run of new highs/lows is exhaustion; fade it on the first opposing reversal bar.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "consecutive_record_exhaustion",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,up_record_count,dn_record_count",
    "long": "After >=8 consecutive lower-low record bars, the current bar prints a bullish reversal (close>open and close>prior close)",
    "short": "After >=8 consecutive higher-high record bars, the current bar prints a bearish reversal (close<open and close<prior close)",
    "desc": "Consecutive new-record exhaustion reversal: a long unbroken run of new highs/lows is exhaustion; fade it on the first opposing reversal bar.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I['open'][i]; c = I['close'][i]; c1 = I['close'][i-1]
    dnr1 = I['dn_record_count'][i-1]
    upr1 = I['up_record_count'][i-1]
    if _nan(o, c, c1, dnr1, upr1):
        return None
    bull_reversal_bar = c > o and c > c1
    bear_reversal_bar = c < o and c < c1
    if dnr1 >= 8 and bull_reversal_bar:
        return 'long'
    if upr1 >= 8 and bear_reversal_bar:
        return 'short'
    return None
