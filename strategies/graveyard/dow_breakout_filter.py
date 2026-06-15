#!/usr/bin/env python3
"""dow_breakout_filter -- Weekday-Gated Volatility Breakout: half prior-day-range breakout off the session open, permitted to go long only early week (Mon/Tue/Wed) and short only late week (Thu/Fri).. tier2 (book-extracted from sister-lab catalog_books).

book:seasonality-time. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "dow_breakout_filter",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "seasonality",
    "tf": "1h-4h",
    "indicators": "Close, day open, prior-day high/low, day-of-week",
    "long": "Close breaks above day open + 0.5x prior-day range on Mon/Tue/Wed",
    "short": "Close breaks below day open - 0.5x prior-day range on Thu/Fri",
    "desc": "Weekday-Gated Volatility Breakout: half prior-day-range breakout off the session open, permitted to go long only early week (Mon/Tue/Wed) and short only late week (Thu/Fri).",
    "source": "book:seasonality-time",
}


def signal(I, i, htf=None):
    if i < 0:
        return None
    c = I["close"][i]
    do = I["day_open"][i]
    dhh = I["prev_dhh"][i]
    dll = I["prev_dll"][i]
    d = I["dow"][i]
    if _nan(c, do, dhh, dll, d):
        return None
    range_y = dhh - dll
    long_trig = c > do + 0.5 * range_y
    short_trig = c < do - 0.5 * range_y
    # dow = ISO weekday Mon=0..Sun=6 (UTC). Longs allowed Mon/Tue/Wed, shorts Thu/Fri.
    if long_trig and d in (0.0, 1.0, 2.0):
        return "long"
    if short_trig and d in (3.0, 4.0):
        return "short"
    return None
