#!/usr/bin/env python3
"""kama_atr_trend_long -- KAMA cross with rising KAMA slope + ATR stop; two-way for FX. David Borst/Perry Kaufman."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "kama_atr_trend_long",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "kama, atr, close",
    "long": "close > kama AND kama rising AND close > close[1] (consecutive bullish closes)",
    "short": "close < kama AND kama falling AND close < close[1] (consecutive bearish closes)",
    "desc": "Kaufman KAMA + ATR trend: close crosses KAMA with rising slope and back-to-back momentum bar",
    "source": "David Borst Medium (datadave1.medium.com); Perry Kaufman Trading Systems and Methods (2013)",
}


def signal(ind, pos, htf=None):
    """Long when close clears rising KAMA on consecutive momentum bars; symmetric short for FX."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    k = ind["kama"][pos]
    k1 = ind["kama"][pos - 1]
    if nan(c, c1, k, k1):
        return None
    kama_rising = k > k1
    kama_falling = k < k1
    if c > k and kama_rising and c > c1:
        return "long"
    if c < k and kama_falling and c < c1:
        return "short"
    return None
