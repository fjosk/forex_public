#!/usr/bin/env python3
"""demark_sequential -- DeMark Sequential buy-countdown completion (long-only here: the mirrored sell countdown is not precomputed, so the short leg is omitted).. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "demark_sequential",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "close,high,low,dm_buy_countdown",
    "long": "DeMark TD buy countdown completes (dm_buy_countdown reaches 13 from below)",
    "short": "## Indicators",
    "desc": "DeMark Sequential buy-countdown completion (long-only here: the mirrored sell countdown is not precomputed, so the short leg is omitted).",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    # Long side only: dm_buy_countdown (TD buy countdown completing at 13) is the
    # sole precomputed DeMark sequence. There is no dm_sell_countdown / sell_countdown
    # array in the engine, so the mirrored short trigger cannot be evaluated and is
    # dropped (kept causal/long-only rather than fabricated). See unknown_keys.
    if i < 1:
        return None
    cd = I['dm_buy_countdown'][i]; cd1 = I['dm_buy_countdown'][i-1]
    if _nan(cd, cd1):
        return None
    if cd >= 13 and cd1 < 13:
        return 'long'
    return None
