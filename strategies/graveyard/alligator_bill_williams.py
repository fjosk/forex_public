#!/usr/bin/env python3
"""alligator_bill_williams -- Bill Williams Alligator (Lips/Teeth/Jaw) trend-eating signal.

Lips crosses above Teeth with all three lines expanding upward = trend eating long.
Lips crosses below Teeth with lines expanding downward = trend eating short.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "alligator_bill_williams",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "al_lips, al_teeth, al_jaw",
    "long": "al_lips crosses above al_teeth with all lines aligned upward (alligator eating up)",
    "short": "al_lips crosses below al_teeth with all lines aligned downward",
    "desc": "Bill Williams Alligator Lips/Teeth/Jaw trend entry",
    "source": "web:https://fxopen.com/blog/en/williams-alligator-strategies/",
}


def signal(ind, pos, htf=None):
    """Alligator lips/teeth cross with expansion filter."""
    lips = ind["al_lips"][pos]
    teeth = ind["al_teeth"][pos]
    jaw = ind["al_jaw"][pos]
    lips1 = ind["al_lips"][pos - 1]
    teeth1 = ind["al_teeth"][pos - 1]
    if nan(lips, teeth, jaw, lips1, teeth1):
        return None
    expanding_up = lips > teeth > jaw
    expanding_dn = lips < teeth < jaw
    if _xup(lips, lips1, teeth, teeth1) and expanding_up:
        return "long"
    if _xdn(lips, lips1, teeth, teeth1) and expanding_dn:
        return "short"
    return None
