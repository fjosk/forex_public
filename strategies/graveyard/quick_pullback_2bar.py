#!/usr/bin/env python3
"""quick_pullback_2bar -- 2-bar inside structure then breakout close. Kevin Davey entry #32."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "quick_pullback_2bar",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "high, low, close",
    "long": "high[-2]>high[-1] AND low[-2]<low[-1] AND close>high[-2]",
    "short": "low[-2]<low[-1] AND high[-2]>high[-1] AND close<low[-2]",
    "desc": "Quick Pullback: 2-bar inside structure followed by breakout close; Kevin Davey #32",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/quick_pullback.html",
}


def signal(ind, pos, htf=None):
    """2-bar inside structure then breakout close."""
    c = ind["close"][pos]
    hi0 = ind["high"][pos]
    lo0 = ind["low"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    hi2 = ind["high"][pos - 2]
    lo2 = ind["low"][pos - 2]
    if nan(c, hi0, lo0, hi1, lo1, hi2, lo2):
        return None
    # Long: 2-bar pattern collapsed then closes above the 2-bar high
    if hi2 > hi1 and lo2 < lo1 and c > hi2:
        return "long"
    # Short: 2-bar pattern collapsed then closes below the 2-bar low
    if lo2 < lo1 and hi2 > hi1 and c < lo2:
        return "short"
    return None
