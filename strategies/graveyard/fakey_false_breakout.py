#!/usr/bin/env python3
"""fakey_false_breakout -- Inside bar false breakout (Fakey): false break then reversal. web:priceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "fakey_false_breakout",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "high, low, close",
    "long": "inside bar at pos-2/pos-1, pos-1 breaks below mother bar low but closes back inside (bull fakey)",
    "short": "inside bar at pos-2/pos-1, pos-1 breaks above mother bar high but closes back inside (bear fakey)",
    "desc": "Fakey false breakout: inside bar false break then reversal",
    "source": "web:https://priceaction.com/price-action-university/strategies/fakey/",
}


def signal(ind, pos, htf=None):
    """Fakey: inside bar then false breakout bar that closes back inside mother."""
    # pos-2 = mother bar, pos-1 = inside bar, pos = false-break bar
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    hi0, lo0, c0 = ind["high"][pos], ind["low"][pos], ind["close"][pos]
    if nan(hi2, lo2, hi1, lo1, c1, hi0, lo0, c0):
        return None
    # Inside bar: pos-1 fully inside pos-2
    inside_bar = hi1 < hi2 and lo1 > lo2
    if not inside_bar:
        return None
    # Bull fakey: current bar broke below inside bar low but closed back above inside bar low
    if lo0 < lo2 and c0 > lo1:
        return "long"
    # Bear fakey: current bar broke above inside bar high but closed back below inside bar high
    if hi0 > hi2 and c0 < hi1:
        return "short"
    return None
