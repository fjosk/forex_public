#!/usr/bin/env python3
"""awesome_oscillator_zero_cross_saucer -- AO zero-cross primary + bullish/bearish saucer. je-suis-tm GitHub."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "awesome_oscillator_zero_cross_saucer",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "ao",
    "long": "AO crosses above zero; OR bullish saucer (concave dip in positive territory, third bar rising)",
    "short": "AO crosses below zero; OR bearish saucer (concave peak in negative territory, third bar falling)",
    "desc": "Awesome Oscillator zero-cross and saucer pattern (3-bar concave confirmation)",
    "source": "je-suis-tm/quant-trading GitHub; Nikhil-Adithyan AO implementation",
}


def signal(ind, pos, htf=None):
    """AO zero-cross or 3-bar saucer pattern momentum signal."""
    ao = ind["ao"][pos]
    ao1 = ind["ao"][pos - 1]
    ao2 = ind["ao"][pos - 2]
    if nan(ao, ao1, ao2):
        return None
    # Zero-line cross
    if ao > 0 and ao1 <= 0:
        return "long"
    if ao < 0 and ao1 >= 0:
        return "short"
    # Bullish saucer: all three bars above zero, second bar is lowest (concave), third rising
    if ao > 0 and ao1 > 0 and ao2 > 0 and ao > ao1 and ao1 < ao2:
        return "long"
    # Bearish saucer: all three bars below zero, second bar is highest (concave), third falling
    if ao < 0 and ao1 < 0 and ao2 < 0 and ao < ao1 and ao1 > ao2:
        return "short"
    return None
