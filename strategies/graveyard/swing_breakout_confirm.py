#!/usr/bin/env python3
"""swing_breakout_confirm -- Williams short-term swing-point confirmation breakout: a confirmed 5-bar fractal marks a swing pivot; a close breaking that pivot's extreme confirms a directional breakout. Trigger levels carry forwar. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "swing_breakout_confirm",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close, frac_dn_bar_high, frac_up_bar_low",
    "long": "Close crosses up through the high of the most recent confirmed down-fractal swing point",
    "short": "Close crosses down through the low of the most recent confirmed up-fractal swing point",
    "desc": "Williams short-term swing-point confirmation breakout: a confirmed 5-bar fractal marks a swing pivot; a close breaking that pivot's extreme confirms a directional breakout. Trigger levels carry forwar",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    trig_hi = I["frac_dn_bar_high"][i]
    trig_lo = I["frac_up_bar_low"][i]
    c = I["close"][i]
    c1 = I["close"][i - 1]
    if _nan(c, c1):
        return None
    if not _nan(trig_hi) and c1 <= trig_hi and c > trig_hi:
        return "long"
    if not _nan(trig_lo) and c1 >= trig_lo and c < trig_lo:
        return "short"
    return None
