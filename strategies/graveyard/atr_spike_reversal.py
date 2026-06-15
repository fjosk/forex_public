#!/usr/bin/env python3
"""atr_spike_reversal -- V-reversal fade of volatility exhaustion: an ATR-scaled overshoot of the recent extreme followed by a turn against it.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "atr_spike_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "ATR(14), rolling 10-bar high (hh_n) / low (ll_n)",
    "long": "Prior bar plunged more than 1 ATR below the 10-bar low and this bar makes a higher low (fade the down-spike)",
    "short": "Prior bar spiked more than 1 ATR above the 10-bar high and this bar makes a lower high (fade the up-spike)",
    "desc": "V-reversal fade of volatility exhaustion: an ATR-scaled overshoot of the recent extreme followed by a turn against it.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    K = 1.0
    h, h1 = I["high"][i], I["high"][i-1]
    l, l1 = I["low"][i], I["low"][i-1]
    hh1, ll1, a1 = I["hh_n"][i-1], I["ll_n"][i-1], I["atr"][i-1]
    if _nan(h, h1, l, l1, hh1, ll1, a1):
        return None
    if (h1 - hh1) > K * a1 and h < h1:
        return "short"
    if (ll1 - l1) > K * a1 and l > l1:
        return "long"
    return None
