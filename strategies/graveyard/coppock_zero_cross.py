#!/usr/bin/env python3
"""coppock_zero_cross -- Coppock Curve Zero-Line Cross. zeta-zetra/EURUSD backtest.

Long when Coppock crosses above zero; short when it crosses below.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "coppock_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "coppock",
    "long": "coppock crosses above zero",
    "short": "coppock crosses below zero",
    "desc": "Coppock Curve zero-line crossover (WMA of dual ROC sum)",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/chatgpt/coppock.html",
}


def signal(ind, pos, htf=None):
    """Coppock zero-line cross."""
    cp = ind["coppock"][pos]
    cp1 = ind["coppock"][pos - 1]
    if nan(cp, cp1):
        return None
    if _xup(cp, cp1, 0.0, 0.0):
        return "long"
    if _xdn(cp, cp1, 0.0, 0.0):
        return "short"
    return None
