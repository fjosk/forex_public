#!/usr/bin/env python3
"""coppock_curve_momentum -- Coppock Curve zero-line cross. Edwin Coppock / QuantifiedStrategies.

WMA(10) of [ROC(14) + ROC(11)] pre-computed as the `coppock` key.
Long when coppock crosses above zero; short when it crosses below.
Source: web:https://www.quantifiedstrategies.com/coppock-curve-strategy/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "coppock_curve_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "coppock",
    "long": "coppock crosses above zero from below",
    "short": "coppock crosses below zero from above",
    "desc": "Coppock Curve zero-line crossover: WMA(10) of ROC(14)+ROC(11)",
    "source": "web:https://www.quantifiedstrategies.com/coppock-curve-strategy/",
}


def signal(ind, pos, htf=None):
    """Coppock Curve: zero-line crossover long/short."""
    if pos < 1:
        return None
    cp = ind["coppock"][pos]
    cp1 = ind["coppock"][pos - 1]
    if nan(cp, cp1):
        return None

    if cp > 0.0 and cp1 <= 0.0:
        return "long"
    if cp < 0.0 and cp1 >= 0.0:
        return "short"

    return None
