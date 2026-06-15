#!/usr/bin/env python3
"""dual_ma_countertrend -- Dual-MA counter-signal fade: use the slow SMA50 as trend filter and fade the opposing fast-EMA cross as a pullback entry.. tier2 (book-extracted from sister-lab catalog_books).

book:mean-reversion. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, _xdn, _xup, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dual_ma_countertrend",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "SMA(50), EMA(9), EMA(21)",
    "long": "In an uptrend (close>SMA50), fade the fast bearish EMA9/21 cross",
    "short": "In a downtrend (close<SMA50), fade the fast bullish EMA9/21 cross",
    "desc": "Dual-MA counter-signal fade: use the slow SMA50 as trend filter and fade the opposing fast-EMA cross as a pullback entry.",
    "source": "book:mean-reversion",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, s50 = I["close"][i], I["sma50"][i]
    e9, e9p = I["ema9"][i], I["ema9"][i-1]
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    if _nan(c, s50, e9, e9p, e21, e21p):
        return None
    trend_up = c > s50
    trend_dn = c < s50
    fast_cross_dn = _xdn(e9, e9p, e21, e21p)
    fast_cross_up = _xup(e9, e9p, e21, e21p)
    if trend_up and fast_cross_dn:
        return "long"
    if trend_dn and fast_cross_up:
        return "short"
    return None
