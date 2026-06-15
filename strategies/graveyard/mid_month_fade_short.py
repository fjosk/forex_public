#!/usr/bin/env python3
"""mid_month_fade_short -- Mid-Month Day-Position Fade: specific trading-day-of-month ordinals (12 short, 18/22 long) as seasonal inflection points, gated by close stretch versus SMA20.. tier2 (book-extracted from sister-lab catalog_books).

book:seasonality-time. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "mid_month_fade_short",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "seasonality",
    "tf": "1d",
    "indicators": "Close, SMA(20), trading-day-of-month (tdm)",
    "long": "On trading-day 18 or 22 while below SMA20 (late-month mean reversion up)",
    "short": "On trading-day 12 while above SMA20 (mid-month fade down)",
    "desc": "Mid-Month Day-Position Fade: specific trading-day-of-month ordinals (12 short, 18/22 long) as seasonal inflection points, gated by close stretch versus SMA20.",
    "source": "book:seasonality-time",
}


def signal(I, i, htf=None):
    if i < 0:
        return None
    t = I["tdm"][i]
    c = I["close"][i]
    m = I["sma20"][i]
    if _nan(t, c, m):
        return None
    # tdm = 1-based trading-day-of-month index (UTC). Specific day ordinals act as
    # inflection points, gated by stretch vs SMA20.
    if t == 12.0 and c > m:
        return "short"
    if t in (18.0, 22.0) and c < m:
        return "long"
    return None
