#!/usr/bin/env python3
"""gap_climax_reversal -- Volatility-climax gap reversal: fade an exhaustion gap when the bar closes against it on an ATR spike.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "gap_climax_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "day_open, prev_dll, prev_dhh, atr_pct, close, high, low",
    "long": "Vol spike + gap below prior-day low + strong close (top third) -> long",
    "short": "Vol spike + gap above prior-day high + weak close (bottom third) -> short",
    "desc": "Volatility-climax gap reversal: fade an exhaustion gap when the bar closes against it on an ATR spike.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 5:
        return None
    ap, ap5 = I["atr_pct"][i], I["atr_pct"][i-5]
    do = I["day_open"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    c, hi, lo = I["close"][i], I["high"][i], I["low"][i]
    if _nan(ap, ap5, do, pdll, pdhh, c, hi, lo):
        return None
    vol_spike = ap > 1.8 * ap5
    rng = max(hi - lo, 1e-9)
    close_pos = (c - lo) / rng
    if vol_spike and do < pdll and close_pos >= 0.66:    # gap down on a vol climax, closing strong off the low -> long
        return "long"
    if vol_spike and do > pdhh and close_pos <= 0.34:    # gap up on a vol climax, closing weak off the high -> short
        return "short"
    return None
