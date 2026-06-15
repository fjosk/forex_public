#!/usr/bin/env python3
"""body_momentum_dominance -- Body Momentum (14-bar white vs black candle-body dominance) oscillator crossing its 70/20 thresholds. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "body_momentum_dominance",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "oscillator",
    "tf": "1h-4h",
    "indicators": "body_mom",
    "long": "Body Momentum oscillator crosses up above 70 (white-body dominance)",
    "short": "Body Momentum oscillator crosses down below 20 (black-body dominance)",
    "desc": "Body Momentum (14-bar white vs black candle-body dominance) oscillator crossing its 70/20 thresholds",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    b = I["body_mom"][i]
    b1 = I["body_mom"][i-1]
    if _nan(b, b1):
        return None
    if b > 70 and b1 <= 70:
        return "long"
    if b < 20 and b1 >= 20:
        return "short"
    return None
