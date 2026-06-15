#!/usr/bin/env python3
"""demark_range_projection -- DeMark projected trading range support/resistance: the prior bar's open-vs-close bias projects a high and low band; a wick-pierce that closes back inside the band is a fade. projLo reconstructed causa. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "demark_range_projection",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h-4h",
    "indicators": "open, high, low, close, dm_proj_hi",
    "long": "Bar pierces the DeMark projected-low (low<=projLo) but closes back above it",
    "short": "Bar pierces the DeMark projected-high (high>=projHi) but closes back below it",
    "desc": "DeMark projected trading range support/resistance: the prior bar's open-vs-close bias projects a high and low band; a wick-pierce that closes back inside the band is a fade. projLo reconstructed causa",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    o = I["open"][i]
    c = I["close"][i]
    lo = I["low"][i]
    hi = I["high"][i]
    pH = I["dm_proj_hi"][i]
    ph = I["high"][i - 1]
    pl = I["low"][i - 1]
    if _nan(o, c, lo, hi, pH, ph, pl):
        return None
    # dm_proj_lo is not precomputed; reconstruct causally.
    # dm_proj_hi = X - prev_low ; dm_proj_lo = X - prev_high
    # => dm_proj_lo = dm_proj_hi - (prev_high - prev_low)
    pL = pH - (ph - pl)
    if lo <= pL and c > pL:
        return "long"
    if hi >= pH and c < pH:
        return "short"
    return None
