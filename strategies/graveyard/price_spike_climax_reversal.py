#!/usr/bin/env python3
"""price_spike_climax_reversal -- Climax spike high/low reversal with ATR magnitude filter. the_new_market_wizards.

Spike low (low sharply below both neighbors by > 1.5*ATR) confirmed after right bar: go long.
Spike high (high sharply above both neighbors by > 1.5*ATR) confirmed after right bar: go short.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "price_spike_climax_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "high,low,close,atr",
    "long": "middle bar low < left low AND right low (spike low by >1.5 ATR); current bar confirms (right bar closed)",
    "short": "middle bar high > left high AND right high (spike high by >1.5 ATR); current bar confirms",
    "desc": "Climax spike reversal: bar with spike high/low versus both neighbors (ATR-filtered fractal)",
    "source": "the_new_market_wizards, Glossary: Spike",
}


def signal(ind, pos, htf=None):
    """Climax spike high/low reversal confirmed after the right bar closes."""
    if pos < 2:
        return None
    # Check spike at bar pos-1 (middle), pos-2 is left, pos is right (confirming)
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    atr = ind["atr"][pos]
    if nan(h1, l1, h2, l2, h, l, c, atr):
        return None
    margin = 1.5 * atr
    # Spike low: l1 is well below both neighbors
    if l1 < l2 - margin and l1 < l - margin:
        return "long"
    # Spike high: h1 is well above both neighbors
    if h1 > h2 + margin and h1 > h + margin:
        return "short"
    return None
