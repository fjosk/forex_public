#!/usr/bin/env python3
"""sr_role_reversal_retest -- Broken support/resistance role-reversal retest using the prior Williams-fractal price level.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "sr_role_reversal_retest",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "Williams fractal levels (frac_up_px/frac_dn_px), close, high, low",
    "long": "Broke above prior fractal resistance, retests it as support and holds",
    "short": "Broke below prior fractal support, retests it as resistance and rejects",
    "desc": "Broken support/resistance role-reversal retest using the prior Williams-fractal price level.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    c, c2 = I['close'][i], I['close'][i-2]
    lo, hi = I['low'][i], I['high'][i]
    res, sup = I['frac_up_px'][i-2], I['frac_dn_px'][i-2]
    if _nan(c, c2, lo, hi, res, sup):
        return None
    if c2 > res and lo <= res * 1.001 and c > res:
        return 'long'
    if c2 < sup and hi >= sup * 0.999 and c < sup:
        return 'short'
    return None
