#!/usr/bin/env python3
"""tema_price_cross -- Price crosses TEMA21 trend filter. AlgoTest Pine / Patrick Mulloy TEMA.

Long when close crosses above tema21. Short when close crosses below tema21.
Uses tema21 (21-period TEMA, available) as the closest substitute for the source's 14-period TEMA.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "tema_price_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "tema21, close",
    "long": "close crosses above tema21",
    "short": "close crosses below tema21",
    "desc": "Price crossover of TEMA21; low-lag trend entry; Patrick Mulloy TEMA concept",
    "source": "web:https://docs.algotest.in/signals/pinescripts/tema_strategy/",
}


def signal(ind, pos, htf=None):
    """Close crosses above/below TEMA21."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    t = ind["tema21"][pos]
    t1 = ind["tema21"][pos - 1]
    if nan(c, c1, t, t1):
        return None
    if _xup(c, c1, t, t1):
        return "long"
    if _xdn(c, c1, t, t1):
        return "short"
    return None
