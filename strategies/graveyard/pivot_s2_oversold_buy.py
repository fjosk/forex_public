#!/usr/bin/env python3
"""pivot_s2_oversold_buy -- Deep-pivot (S2/R2) oversold/overbought reaction: fade extreme pivot tags confirmed by momentum.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_s2_oversold_buy",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_reversion",
    "tf": "1h (UTC-day)",
    "indicators": "Deep pivots S2/R2, RSI(14), Stochastic %K, close, high, low",
    "long": "Tag S2 and close back above with RSI<35 and Stoch %K<25 (oversold)",
    "short": "Tag R2 and close back below with RSI>65 and Stoch %K>75 (overbought)",
    "desc": "Deep-pivot (S2/R2) oversold/overbought reaction: fade extreme pivot tags confirmed by momentum.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    s2, r2 = I['piv_s2'][i], I['piv_r2'][i]
    lo, hi, c = I['low'][i], I['high'][i], I['close'][i]
    rsi, k = I['rsi'][i], I['stoch_k'][i]
    if _nan(s2, r2, lo, hi, c, rsi, k):
        return None
    if lo <= s2 and c > s2 and rsi < 35 and k < 25:
        return 'long'
    if hi >= r2 and c < r2 and rsi > 65 and k > 75:
        return 'short'
    return None
