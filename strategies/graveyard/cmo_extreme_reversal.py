#!/usr/bin/env python3
"""cmo_extreme_reversal -- Chande Momentum Oscillator extreme reversal: enter as CMO turns back from a +/-50 extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "cmo_extreme_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h-4h",
    "indicators": "CMO(14)",
    "long": "CMO <= -50 last bar and turning up this bar",
    "short": "CMO >= 50 last bar and turning down this bar",
    "desc": "Chande Momentum Oscillator extreme reversal: enter as CMO turns back from a +/-50 extreme.",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    cm, cm1 = I["cmo"][i], I["cmo"][i-1]
    if _nan(cm, cm1):
        return None
    if cm1 <= -50 and cm > cm1:               # CMO turning up out of oversold extreme
        return "long"
    if cm1 >= 50 and cm < cm1:                 # CMO turning down out of overbought extreme
        return "short"
    return None
