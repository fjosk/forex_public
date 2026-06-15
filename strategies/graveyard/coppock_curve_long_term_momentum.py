#!/usr/bin/env python3
"""coppock_curve_long_term_momentum -- Coppock Curve zero-line crossover. StockCharts / Edwin Coppock (1962).

Coppock crosses above zero = long-term momentum recovery signal (long).
Crosses below zero = bearish (short, lower-confidence per original design).
Best on weekly/daily with long-period bars; the engine key uses the standard period.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "coppock_curve_long_term_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "coppock",
    "long": "Coppock Curve crosses above zero from below",
    "short": "Coppock Curve crosses below zero from above",
    "desc": "Coppock Curve long-term momentum zero-line crossover (Edwin Coppock 1962)",
    "source": "web:https://chartschool.stockcharts.com coppock-curve",
}

_ZERO = 0.0


def signal(ind, pos, htf=None):
    """Coppock zero-line cross."""
    cop = ind["coppock"][pos]
    cop1 = ind["coppock"][pos - 1]
    if nan(cop, cop1):
        return None
    if _xup(cop, cop1, _ZERO, _ZERO):
        return "long"
    if _xdn(cop, cop1, _ZERO, _ZERO):
        return "short"
    return None
