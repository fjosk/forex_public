#!/usr/bin/env python3
"""time_series_momentum_12_1 -- Time-Series Momentum 12-1 (Moskowitz/Ooi/Pedersen 2012).
web:https://quantpedia.com/strategies/time-series-momentum-effect
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "time_series_momentum_12_1",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "daily",
    "indicators": "close",
    "long": "12-month return minus 1-month return is positive (tsmom > 0)",
    "short": "12-month return minus 1-month return is negative (tsmom < 0)",
    "desc": "Time-series momentum: sign of 252-bar minus 21-bar cumulative return determines direction",
    "source": "web:https://quantpedia.com/strategies/time-series-momentum-effect Moskowitz/Ooi/Pedersen 2012",
}


def signal(ind, pos, htf=None):
    """TSMOM 12-1: 252-bar return minus 21-bar return; long if positive, short if negative."""
    if pos < 252:
        return None
    c = ind["close"][pos]
    c21 = ind["close"][pos - 21]
    c252 = ind["close"][pos - 252]
    if nan(c, c21, c252) or c252 == 0 or c21 == 0:
        return None
    r_12 = (c - c252) / c252
    r_1 = (c - c21) / c21
    tsmom = r_12 - r_1
    if tsmom > 0:
        return "long"
    if tsmom < 0:
        return "short"
    return None
