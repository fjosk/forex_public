#!/usr/bin/env python3
"""false_break_failure_fade -- Fades a failed Donchian channel breakout: a recent bar pierced the channel but price closed back inside and reverses.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "false_break_failure_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "Donchian(up/lo)",
    "long": "Recent poke above Donchian upper fails (back below) and close < prior close",
    "short": "Recent poke below Donchian lower fails (back above) and close > prior close",
    "desc": "Fades a failed Donchian channel breakout: a recent bar pierced the channel but price closed back inside and reverses.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 4:
        return None
    h, l, c, du, dl = I["high"], I["low"], I["close"], I["dc_up"], I["dc_lo"]
    if _nan(c[i], c[i-1]):
        return None
    # any bar in i-3..i-1 poked above the PRIOR-bar dc_up, but price is now back below dc_up
    fake_up = any((not _nan(h[j], du[j-1])) and h[j] > du[j-1] for j in range(i-3, i)) \
        and (not _nan(du[i])) and c[i] < du[i]
    fake_dn = any((not _nan(l[j], dl[j-1])) and l[j] < dl[j-1] for j in range(i-3, i)) \
        and (not _nan(dl[i])) and c[i] > dl[i]
    if fake_up and c[i] < c[i-1]:
        return "short"
    if fake_dn and c[i] > c[i-1]:
        return "long"
    return None
