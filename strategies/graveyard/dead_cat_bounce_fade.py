#!/usr/bin/env python3
"""dead_cat_bounce_fade -- Inverted dead-cat-bounce: fade an over-extended single-bar move sized to an ATR-normalized, floor-5% threshold.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "dead_cat_bounce_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "ROC, ATR%",
    "long": "ROC spikes down at least max(5%, 4xATR%) -- fade the crash, expect a bounce",
    "short": "ROC spikes up at least max(5%, 4xATR%) -- fade the spike, expect mean reversion",
    "desc": "Inverted dead-cat-bounce: fade an over-extended single-bar move sized to an ATR-normalized, floor-5% threshold.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    r, ap = I["roc"][i], I["atr_pct"][i]
    if _nan(r, ap):
        return None
    thr = max(5.0, 4.0 * ap * 100.0)
    if r >= thr:
        return "short"
    if r <= -thr:
        return "long"
    return None
