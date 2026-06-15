#!/usr/bin/env python3
"""pivot_ma_confluence_reversal -- Pivot + EMA confluence reaction: react off a support/resistance level reinforced by an EMA20/50 cluster.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_ma_confluence_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h (UTC-day)",
    "indicators": "Pivot S1/R1, EMA20, EMA50, close, high, low",
    "long": "S1 coincides with EMA20/50 (within 0.4%) and price tags then closes above S1",
    "short": "R1 coincides with EMA20/50 (within 0.4%) and price tags then closes below R1",
    "desc": "Pivot + EMA confluence reaction: react off a support/resistance level reinforced by an EMA20/50 cluster.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    s1, r1 = I['piv_s1'][i], I['piv_r1'][i]
    e20, e50 = I['ema20'][i], I['ema50'][i]
    c, lo, hi = I['close'][i], I['low'][i], I['high'][i]
    if _nan(s1, r1, e20, e50, c, lo, hi):
        return None
    tol = 0.004 * c
    if (abs(s1 - e20) <= tol or abs(s1 - e50) <= tol) and lo <= s1 and c > s1:
        return 'long'
    if (abs(r1 - e20) <= tol or abs(r1 - e50) <= tol) and hi >= r1 and c < r1:
        return 'short'
    return None
