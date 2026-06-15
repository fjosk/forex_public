#!/usr/bin/env python3
"""ema20_sma100_macd_breakout -- Dual-MA reclaim/break-down confirmed by a recent MACD histogram zero-cross (momentum-confirmed trend re-entry).. tier2 (book-extracted from sister-lab catalog_books).

book:momentum. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "ema20_sma100_macd_breakout",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "EMA(20), SMA(100), MACD histogram",
    "long": "Close reclaims above both EMA20 and SMA100 with a bullish MACD-hist flip in the last 5 bars",
    "short": "Close breaks below both EMA20 and SMA100 with a bearish MACD-hist flip in the last 5 bars",
    "desc": "Dual-MA reclaim/break-down confirmed by a recent MACD histogram zero-cross (momentum-confirmed trend re-entry).",
    "source": "book:momentum",
}


def signal(I, i, htf=None):
    if i < 6:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    e20, e201 = I["ema20"][i], I["ema20"][i-1]
    s100, s1001 = I["sma100"][i], I["sma100"][i-1]
    if _nan(c, c1, e20, e201, s100, s1001):
        return None
    crossed_up = c > e20 and c > s100 and (c1 <= e201 or c1 <= s1001)
    crossed_dn = c < e20 and c < s100 and (c1 >= e201 or c1 >= s1001)
    macd_up_recent = False
    macd_dn_recent = False
    for k in range(0, 5):
        h0, hm1 = I["macd_hist"][i-k], I["macd_hist"][i-k-1]
        if _nan(h0, hm1):
            continue
        if h0 > 0 and hm1 <= 0:
            macd_up_recent = True
        if h0 < 0 and hm1 >= 0:
            macd_dn_recent = True
    if crossed_up and macd_up_recent:
        return "long"
    if crossed_dn and macd_dn_recent:
        return "short"
    return None
