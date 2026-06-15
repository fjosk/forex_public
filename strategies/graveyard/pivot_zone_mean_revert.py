#!/usr/bin/env python3
"""pivot_zone_mean_revert -- Floor-pivot inner-zone mean reversion (Jackson/Gould): fade toward the pivot from inside the S1-P / P-R1 band.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_zone_mean_revert",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h (UTC-day)",
    "indicators": "Classic pivots P/S1/R1, close, high, low",
    "long": "In lower pivot zone (S1<close<P), close up and tagged below prior close",
    "short": "In upper pivot zone (P<close<R1), close down and tagged above prior close",
    "desc": "Floor-pivot inner-zone mean reversion (Jackson/Gould): fade toward the pivot from inside the S1-P / P-R1 band.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    p, s1, r1 = I['piv_p'][i], I['piv_s1'][i], I['piv_r1'][i]
    c, c1 = I['close'][i], I['close'][i-1]
    lo, hi = I['low'][i], I['high'][i]
    if _nan(p, s1, r1, c, c1, lo, hi):
        return None
    if s1 < c < p and c > c1 and lo < c1:
        return 'long'
    if p < c < r1 and c < c1 and hi > c1:
        return 'short'
    return None
