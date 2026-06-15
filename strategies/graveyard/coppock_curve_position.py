#!/usr/bin/env python3
"""coppock_curve_position -- Coppock Curve zero-cross with trough confirmation. RobustTrader."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "coppock_curve_position",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "weekly/monthly",
    "indicators": "coppock",
    "long": "Coppock crosses above zero AND was below zero 2 bars prior (trough confirmation)",
    "short": "Coppock crosses below zero (exit long / no original short)",
    "desc": "Coppock Curve position trade: zero-cross with prior trough confirmation",
    "source": "web:https://therobusttrader.com/coppock-curve/",
}


def signal(ind, pos, htf=None):
    """Coppock position: cross above zero after a trough (was below at pos-2)."""
    if pos < 2:
        return None
    cop0 = ind["coppock"][pos]
    cop1 = ind["coppock"][pos - 1]
    cop2 = ind["coppock"][pos - 2]
    if nan(cop0, cop1, cop2):
        return None

    # Long: cross above zero AND was in trough (below zero 2 bars ago)
    if cop0 > 0 and cop1 <= 0 and cop2 < 0:
        return "long"

    # Short (theoretical mirror): cross below zero
    if cop0 < 0 and cop1 >= 0:
        return "short"

    return None
