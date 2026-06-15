#!/usr/bin/env python3
"""wide_bar_narrow_rest_break -- Wide-range bar followed by a tight two-bar rest cluster, then a break of the cluster extreme in the wide bar's direction.. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "wide_bar_narrow_rest_break",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,rng_sma20",
    "long": "Bullish wide-range bar (range>1.5x avg), two narrow inside-rest bars holding above its low, then close-bar high breaks the rest cluster high",
    "short": "Bearish wide-range bar, two narrow rest bars holding below its high, then low breaks the rest cluster low",
    "desc": "Wide-range bar followed by a tight two-bar rest cluster, then a break of the cluster extreme in the wide bar's direction.",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 3:
        return None
    h, l, o, c = I["high"], I["low"], I["open"], I["close"]
    w = i - 3
    rs = I["rng_sma20"][i]
    if _nan(rs, h[i], l[i], h[w], l[w], o[w], c[w]):
        return None
    rng_w = h[w] - l[w]
    rest_h = [h[k] for k in range(w + 1, i)]
    rest_l = [l[k] for k in range(w + 1, i)]
    if any(_nan(x) for x in rest_h) or any(_nan(x) for x in rest_l):
        return None
    rest_rng = [rh - rl for rh, rl in zip(rest_h, rest_l)]
    rest_narrow = all(r < rng_w for r in rest_rng)
    wide_up = rng_w > 1.5 * rs and c[w] > o[w]
    if wide_up and rest_narrow and min(rest_l) >= l[w] and h[i] > max(rest_h):
        return "long"
    wide_dn = rng_w > 1.5 * rs and c[w] < o[w]
    if wide_dn and rest_narrow and max(rest_h) <= h[w] and l[i] < min(rest_l):
        return "short"
    return None
