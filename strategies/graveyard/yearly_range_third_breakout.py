#!/usr/bin/env python3
"""yearly_range_third_breakout -- Donchian channel breakout filtered by 12-month (252-bar) range position: only take breaks that begin from the far third of the yearly range. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "yearly_range_third_breakout",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "pivot-sr",
    "tf": "1h-4h",
    "indicators": "yr_high,yr_low,dc_up,dc_lo,close",
    "long": "Donchian-upper breakout while still in the lower third of the 12-month range",
    "short": "Donchian-lower breakdown while still in the upper third of the 12-month range",
    "desc": "Donchian channel breakout filtered by 12-month (252-bar) range position: only take breaks that begin from the far third of the yearly range",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    yh = I["yr_high"][i]
    yl = I["yr_low"][i]
    c = I["close"][i]
    c1 = I["close"][i-1]
    dcu = I["dc_up"][i-1]
    dcl = I["dc_lo"][i-1]
    if _nan(yh, yl, c, c1, dcu, dcl) or yh <= yl:
        return None
    rng = yh - yl
    lo_b = yl + rng / 3.0
    hi_b = yl + 2.0 * rng / 3.0
    if c > dcu and c1 <= dcu and c <= lo_b:
        return "long"
    if c < dcl and c1 >= dcl and c >= hi_b:
        return "short"
    return None
