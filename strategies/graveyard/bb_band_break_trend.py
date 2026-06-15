#!/usr/bin/env python3
"""bb_band_break_trend -- Bollinger band-break momentum continuation (a breakout, not a mean-reversion bounce): trade the close pushing through the band.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "bb_band_break_trend",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "Bollinger Bands(20,2)",
    "long": "Close breaks above the upper band (was at/below it last bar)",
    "short": "Close breaks below the lower band (was at/above it last bar)",
    "desc": "Bollinger band-break momentum continuation (a breakout, not a mean-reversion bounce): trade the close pushing through the band.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    bu, bu1 = I["bb_up"][i], I["bb_up"][i-1]
    bl, bl1 = I["bb_lo"][i], I["bb_lo"][i-1]
    if _nan(c, c1, bu, bu1, bl, bl1):
        return None
    if c > bu and c1 <= bu1:
        return "long"
    if c < bl and c1 >= bl1:
        return "short"
    return None
