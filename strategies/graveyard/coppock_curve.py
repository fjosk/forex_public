#!/usr/bin/env python3
"""coppock_curve -- Coppock Curve zero-cross two-sided. EarnForex."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "coppock_curve",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "monthly/weekly",
    "indicators": "coppock",
    "long": "Coppock Curve crosses above zero from below",
    "short": "Coppock Curve crosses below zero from above (cautious)",
    "desc": "Coppock Curve zero-cross oscillator: long on positive cross, short on negative",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Simple Coppock zero-line cross, two-sided."""
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
