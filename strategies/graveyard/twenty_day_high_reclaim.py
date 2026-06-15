#!/usr/bin/env python3
"""twenty_day_high_reclaim -- N-day high failure-and-reclaim: after a recent breakout and pullback, re-entry on a clean reclaim of the rolling 20-bar extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "twenty_day_high_reclaim",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "Donchian(up/lo), OHLC",
    "long": "Recent N-bar high made, pulled back, then reclaims the 20-bar high (close crosses back above)",
    "short": "Recent N-bar low made, bounced, then breaks back below the 20-bar low",
    "desc": "N-day high failure-and-reclaim: after a recent breakout and pullback, re-entry on a clean reclaim of the rolling 20-bar extreme.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 21:
        return None
    h, l, c, du, dl = I["high"], I["low"], I["close"], I["dc_up"], I["dc_lo"]
    if _nan(c[i], c[i-1], l[i-3], h[i-3]):
        return None
    hh_win = [h[k] for k in range(i-20, i)]
    ll_win = [l[k] for k in range(i-20, i)]
    if any(_nan(x) for x in hh_win) or any(_nan(x) for x in ll_win):
        return None
    hh = max(hh_win)
    ll = min(ll_win)
    # long: recently tagged a Donchian high, pulled back, reclaims the 20-bar high THIS bar
    made_high = any((not _nan(h[j], du[j-1])) and h[j] >= du[j-1] for j in range(i-5, i))
    pulled = min(l[i-2], l[i-1], l[i]) < l[i-3]
    reclaim = c[i] > hh and c[i-1] <= hh
    if made_high and pulled and reclaim:
        return "long"
    made_low = any((not _nan(l[j], dl[j-1])) and l[j] <= dl[j-1] for j in range(i-5, i))
    bounced = max(h[i-2], h[i-1], h[i]) > h[i-3]
    reclaim_d = c[i] < ll and c[i-1] >= ll
    if made_low and bounced and reclaim_d:
        return "short"
    return None
