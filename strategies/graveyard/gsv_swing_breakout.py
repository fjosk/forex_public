#!/usr/bin/env python3
"""gsv_swing_breakout -- Williams Greatest Swing Value: open-relative volatility breakout, entry threshold = a multiple of the averaged adverse swing, gated by recent close context.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "gsv_swing_breakout",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,buy_swing,sell_swing",
    "long": "Down-context (close[-1]<close[-6]) and high pierces open + 1.8*buy_swing (SMA of high-open,4)",
    "short": "Up-context (close[-1]>close[-7]) and low pierces open - 1.8*sell_swing (SMA of open-low,4)",
    "desc": "Williams Greatest Swing Value: open-relative volatility breakout, entry threshold = a multiple of the averaged adverse swing, gated by recent close context.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 7:
        return None
    F = 1.8
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]
    c1 = I['close'][i-1]; c6 = I['close'][i-6]; c7 = I['close'][i-7]
    bs = I['buy_swing'][i]; ss = I['sell_swing'][i]
    if _nan(o, h, l, c1, c6, c7, bs, ss):
        return None
    long_setup = c1 < c6
    short_setup = c1 > c7
    if long_setup and h >= o + F * bs:
        return 'long'
    if short_setup and l <= o - F * ss:
        return 'short'
    return None
