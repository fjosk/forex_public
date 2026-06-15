#!/usr/bin/env python3
"""coppock_curve_monthly_longs -- Coppock Curve zero-line cross long-only. QuantifiedStrategies."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "coppock_curve_monthly_longs",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "monthly/weekly",
    "indicators": "coppock",
    "long": "Coppock Curve crosses from below zero to above zero",
    "short": "Coppock Curve crosses from above zero to below zero (theoretical mirror)",
    "desc": "Coppock Curve zero-line cross: bull market bottom detection (long-only original)",
    "source": "web:https://www.quantifiedstrategies.com/coppock-curve-strategy/",
}


def signal(ind, pos, htf=None):
    """Coppock zero-cross: buy when curve turns positive, short on negative cross."""
    if pos < 1:
        return None
    cop0 = ind["coppock"][pos]
    cop1 = ind["coppock"][pos - 1]
    if nan(cop0, cop1):
        return None

    if cop0 > 0 and cop1 <= 0:
        return "long"
    if cop0 < 0 and cop1 >= 0:
        return "short"

    return None
