#!/usr/bin/env python3
"""cmo_trend_momentum -- Chande Momentum Oscillator zero-line crossover. HowToTrade.

CMO(20) crosses above zero from below = upward momentum turn = long.
CMO crosses below zero = short. Exhaustion exit when CMO reaches +/-50.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "cmo_trend_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "cmo",
    "long": "CMO crosses above zero from below",
    "short": "CMO crosses below zero from above",
    "desc": "Chande Momentum Oscillator zero-line crossover trend signal",
    "source": "web:https://howtotrade.com/indicators/chande-momentum-oscillator/",
}

_ZERO = 0.0


def signal(ind, pos, htf=None):
    """CMO zero-line cross."""
    cmo_v = ind["cmo"][pos]
    cmo1 = ind["cmo"][pos - 1]
    if nan(cmo_v, cmo1):
        return None
    if _xup(cmo_v, cmo1, _ZERO, _ZERO):
        return "long"
    if _xdn(cmo_v, cmo1, _ZERO, _ZERO):
        return "short"
    return None
