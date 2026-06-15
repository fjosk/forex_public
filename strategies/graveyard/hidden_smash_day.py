#!/usr/bin/env python3
"""hidden_smash_day -- Williams hidden-smash-day reversal: a hidden close in the bar extreme that gets confirmed by the next bar breaking the setup bar's range.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "hidden_smash_day",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "OHLC",
    "long": "Prior up-bar closed in bottom 25% of its range and below open, then this bar takes out the prior high",
    "short": "Prior down-bar closed in top 25% of its range and above open, then this bar takes out the prior low",
    "desc": "Williams hidden-smash-day reversal: a hidden close in the bar extreme that gets confirmed by the next bar breaking the setup bar's range.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    h1, l1, c1, o1, c2 = I["high"][i-1], I["low"][i-1], I["close"][i-1], I["open"][i-1], I["close"][i-2]
    hi, lo = I["high"][i], I["low"][i]
    if _nan(h1, l1, c1, o1, c2, hi, lo):
        return None
    rng = h1 - l1
    if rng <= 0:
        return None
    buy_setup = c1 > c2 and c1 <= l1 + 0.25 * rng and c1 < o1
    sell_setup = c1 < c2 and c1 >= h1 - 0.25 * rng and c1 > o1
    if buy_setup and hi > h1:
        return "long"
    if sell_setup and lo < l1:
        return "short"
    return None
