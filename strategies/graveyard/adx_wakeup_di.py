#!/usr/bin/env python3
"""adx_wakeup_di -- ADX waking up from a dormant low beneath both DI lines signals a fresh trend; direction taken from the dominant DI.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "adx_wakeup_di",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "ADX(14), +DI(14), -DI(14)",
    "long": "ADX wakes up (>=4 off its 10-bar low, rising) from below both DI lines with +DI > -DI",
    "short": "ADX wakes up from below both DI lines with -DI > +DI",
    "desc": "ADX waking up from a dormant low beneath both DI lines signals a fresh trend; direction taken from the dominant DI.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 11:
        return None
    adx, dp, dm = I["adx"], I["di_plus"], I["di_minus"]
    win = [adx[k] for k in range(i-10, i+1)]
    if any(_nan(x) for x in win):
        return None
    if _nan(adx[i-1], dp[i-1], dm[i-1], dp[i], dm[i]):
        return None
    adx_low = min(win)
    was_below = adx[i-1] < dp[i-1] and adx[i-1] < dm[i-1]
    wake = (adx[i] - adx_low >= 4) and adx[i] > adx[i-1]
    if was_below and wake and dp[i] > dm[i]:
        return "long"
    if was_below and wake and dm[i] > dp[i]:
        return "short"
    return None
