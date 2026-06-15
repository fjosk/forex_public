#!/usr/bin/env python3
"""sniperjaw_alligator_lips_jaw_cross -- Alligator Lips/Jaw crossover EA. MQL4 CodeBase 60015."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "sniperjaw_alligator_lips_jaw_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "al_lips, al_jaw",
    "long": "al_lips crosses above al_jaw (fastest line crosses slowest line upward)",
    "short": "al_lips crosses below al_jaw",
    "desc": "SniperJaw EA: Alligator Lips/Jaw crossover; single-position reversal exit",
    "source": "MQL5 Code Base 60015, author Ranuka (SniperJaw EA, 2025)",
}


def signal(ind, pos, htf=None):
    """Lips crosses above Jaw for long; below Jaw for short."""
    lips = ind["al_lips"][pos]
    jaw = ind["al_jaw"][pos]
    lips1 = ind["al_lips"][pos - 1]
    jaw1 = ind["al_jaw"][pos - 1]
    if nan(lips, jaw, lips1, jaw1):
        return None
    if _xup(lips, lips1, jaw, jaw1):
        return "long"
    if _xdn(lips, lips1, jaw, jaw1):
        return "short"
    return None
