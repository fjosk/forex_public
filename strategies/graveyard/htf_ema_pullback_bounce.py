#!/usr/bin/env python3
"""htf_ema_pullback_bounce -- Elder Screen-2 HTF-trend EMA21 pullback-bounce: trade with the higher-timeframe bias on a pullback touch of a sloping EMA21 that the close reclaims/rejects.. tier2 (book-extracted from sister-lab catalog_books).

book:multi-timeframe. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "htf_ema_pullback_bounce",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "HTF EMA20/50 bias, EMA(21), high/low/close",
    "long": "HTF up + rising EMA21 + low pulls back to EMA21 + close reclaims (close>=prev)",
    "short": "HTF down + falling EMA21 + high rallies to EMA21 + close rejects (close<=prev)",
    "desc": "Elder Screen-2 HTF-trend EMA21 pullback-bounce: trade with the higher-timeframe bias on a pullback touch of a sloping EMA21 that the close reclaims/rejects.",
    "source": "book:multi-timeframe",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    bias = htf["bias"][i]
    e21, e21_1 = I["ema21"][i], I["ema21"][i-1]
    l, h = I["low"][i], I["high"][i]
    c, c1 = I["close"][i], I["close"][i-1]
    if _nan(bias, e21, e21_1, l, h, c, c1):
        return None
    rising = e21 > e21_1
    falling = e21 < e21_1
    if bias > 0 and rising and l <= e21 and c > e21 and c >= c1:
        return "long"   # HTF up, EMA21 rising, pullback touches it, close reclaims + up bar
    if bias < 0 and falling and h >= e21 and c < e21 and c <= c1:
        return "short"  # HTF down, EMA21 falling, rally touches it, close rejects + down bar
    return None
