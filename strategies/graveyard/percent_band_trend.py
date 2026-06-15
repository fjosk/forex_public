#!/usr/bin/env python3
"""percent_band_trend -- Kaufman percentage-of-price band breakout: trade a close crossing a fixed-percent envelope around SMA20.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "percent_band_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "SMA(20), percentage band (+/-3%)",
    "long": "Close crosses above the +3% percentage band",
    "short": "Close crosses below the -3% percentage band",
    "desc": "Kaufman percentage-of-price band breakout: trade a close crossing a fixed-percent envelope around SMA20.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    up, up1 = I["pct_band_up"][i], I["pct_band_up"][i-1]
    lo, lo1 = I["pct_band_lo"][i], I["pct_band_lo"][i-1]
    if _nan(c, c1, up, up1, lo, lo1):
        return None
    if c > up and c1 <= up1:
        return "long"
    if c < lo and c1 >= lo1:
        return "short"
    return None
