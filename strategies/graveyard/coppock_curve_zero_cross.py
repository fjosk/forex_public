#!/usr/bin/env python3
"""coppock_curve_zero_cross -- Coppock curve zero-line crossover (Pring 4-bar confirmation). Nikhil Adithyan."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "coppock_curve_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1d",
    "indicators": "coppock",
    "long": "Coppock crosses above zero AND prior 4 bars all negative (Pring confirmation)",
    "short": "Coppock crosses below zero AND prior 4 bars all positive (Pring confirmation)",
    "desc": "Coppock Curve zero-line cross with Pring 4-consecutive-bar pre-cross filter",
    "source": "Nikhil Adithyan Coppock Python backtest (medium.com/codex); Edwin Coppock oscillator",
}


def signal(ind, pos, htf=None):
    """Coppock zero-cross with 4-bar directional pre-confirmation (Pring rule)."""
    if pos < 5:
        return None
    copp = ind["coppock"]
    c = copp[pos]
    c1 = copp[pos - 1]
    if nan(c, c1):
        return None
    # Enhanced Pring long: prior 4 bars all negative, current crosses above zero
    if c > 0 and c1 <= 0:
        prior_neg = all(not nan(copp[pos - i]) and copp[pos - i] < 0 for i in range(1, 5))
        if prior_neg:
            return "long"
    # Enhanced Pring short: prior 4 bars all positive, current crosses below zero
    if c < 0 and c1 >= 0:
        prior_pos = all(not nan(copp[pos - i]) and copp[pos - i] > 0 for i in range(1, 5))
        if prior_pos:
            return "short"
    return None
