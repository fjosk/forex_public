#!/usr/bin/env python3
"""adx_range_rsi_fade -- Weak-ADX range oscillator fade: only fade extremes when ADX confirms the market is not trending, with a Bollinger-band touch as the trigger.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "adx_range_rsi_fade",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "15m-4h",
    "indicators": "ADX(14), RSI(14), Stochastic %K, Bollinger Bands(20,2)",
    "long": "In a weak-ADX range, RSI<30 or %K<20 and close at/below lower band",
    "short": "In a weak-ADX range, RSI>70 or %K>80 and close at/above upper band",
    "desc": "Weak-ADX range oscillator fade: only fade extremes when ADX confirms the market is not trending, with a Bollinger-band touch as the trigger.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 0:
        return None
    adx, r, k = I["adx"][i], I["rsi"][i], I["stoch_k"][i]
    c, bl, bu = I["close"][i], I["bb_lo"][i], I["bb_up"][i]
    if _nan(adx, r, k, c, bl, bu):
        return None
    ranging = adx < 25
    if ranging and (r < 30 or k < 20) and c <= bl:
        return "long"
    if ranging and (r > 70 or k > 80) and c >= bu:
        return "short"
    return None
