#!/usr/bin/env python3
"""p3t_pivot_stoch_confluence -- Person P3T pivot + Stochastic confluence reversal: a pivot tag confirmed by a stochastic cross out of an extreme.. tier2 (book-extracted from sister-lab catalog_books).

book:multi-timeframe. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "p3t_pivot_stoch_confluence",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h (UTC-day)",
    "indicators": "Pivot S1/R1, Stochastic %K/%D, close, high, low",
    "long": "Tag S1, close above, and Stochastic %K crosses up over %D from oversold (<30)",
    "short": "Tag R1, close below, and Stochastic %K crosses down under %D from overbought (>70)",
    "desc": "Person P3T pivot + Stochastic confluence reversal: a pivot tag confirmed by a stochastic cross out of an extreme.",
    "source": "book:multi-timeframe",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    s1, r1 = I['piv_s1'][i], I['piv_r1'][i]
    lo, hi, c = I['low'][i], I['high'][i], I['close'][i]
    k, k1 = I['stoch_k'][i], I['stoch_k'][i-1]
    d, d1 = I['stoch_d'][i], I['stoch_d'][i-1]
    if _nan(s1, r1, lo, hi, c, k, k1, d, d1):
        return None
    if lo <= s1 and c > s1 and k1 < 30 and k1 <= d1 and k > d:
        return 'long'
    if hi >= r1 and c < r1 and k1 > 70 and k1 >= d1 and k < d:
        return 'short'
    return None
