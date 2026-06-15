#!/usr/bin/env python3
"""stoch_extreme_touch_trend_gated -- Stochastic extreme touch used as a with-trend entry, EMA21 slope as the no-go filter.. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "stoch_extreme_touch_trend_gated",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "Stochastic %K(14), EMA(21)",
    "long": "EMA21 rising and %K <= 15 (oversold touch with-trend)",
    "short": "EMA21 falling and %K >= 85 (overbought touch with-trend)",
    "desc": "Stochastic extreme touch used as a with-trend entry, EMA21 slope as the no-go filter.",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    k = I["stoch_k"][i]
    if _nan(e21, e21p, k):
        return None
    ema_up = e21 > e21p
    if ema_up and k <= 15:                    # buy oversold dips only when EMA21 is rising
        return "long"
    if (not ema_up) and k >= 85:               # sell overbought pops only when EMA21 is falling
        return "short"
    return None
