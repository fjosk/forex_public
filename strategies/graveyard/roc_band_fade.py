#!/usr/bin/env python3
"""roc_band_fade -- Momentum SD-band countertrend fade: when rate-of-change pierces a 2-sigma band and rolls back, fade the extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "roc_band_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "roc,roc_sd",
    "long": "ROC was below -2*rolling_std(ROC,100) and turns up",
    "short": "ROC was above +2*rolling_std(ROC,100) and turns down",
    "desc": "Momentum SD-band countertrend fade: when rate-of-change pierces a 2-sigma band and rolls back, fade the extreme.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    r = I['roc'][i]; r1 = I['roc'][i-1]; sd = I['roc_sd'][i]
    if _nan(r, r1, sd):
        return None
    upper = 2.0 * sd
    lower = -2.0 * sd
    if r1 < lower and r > r1:
        return 'long'
    if r1 > upper and r < r1:
        return 'short'
    return None
