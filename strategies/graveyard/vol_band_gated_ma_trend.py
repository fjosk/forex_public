#!/usr/bin/env python3
"""vol_band_gated_ma_trend -- Volatility-band activity-window filter: only act on an SMA50 slope turn when the bar's absolute change sits in the normal activity band (not dead, not a blow-off).. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "vol_band_gated_ma_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "SMA(50), abs price change (abschg), volatility band (vavg/vsd, 35)",
    "long": "Activity inside the volatility band and SMA50 slope turns up",
    "short": "Activity inside the volatility band and SMA50 slope turns down",
    "desc": "Volatility-band activity-window filter: only act on an SMA50 slope turn when the bar's absolute change sits in the normal activity band (not dead, not a blow-off).",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    va, vd, ac = I["vavg"][i], I["vsd"][i], I["abschg"][i]
    s, s1, s2 = I["sma50"][i], I["sma50"][i-1], I["sma50"][i-2]
    if _nan(va, vd, ac, s, s1, s2):
        return None
    low_lim = va - vd
    high_lim = va + 2.0 * vd
    if not (ac > low_lim and ac < high_lim):
        return None
    if s > s1 and s1 <= s2:
        return "long"
    if s < s1 and s1 >= s2:
        return "short"
    return None
