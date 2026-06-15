#!/usr/bin/env python3
"""tsi_swing_daily -- TSI crosses above/below signal line above/below zero. AronGroups."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "tsi_swing_daily",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "daily",
    "indicators": "tsi, tsi_sig",
    "long": "TSI crosses above signal line AND TSI above zero",
    "short": "TSI crosses below signal line AND TSI below zero",
    "desc": "TSI True Strength Index: signal-line cross with zero-line momentum confirmation",
    "source": "web:https://arongroups.co/technical-analyze/true-strength-index-tsi/",
}


def signal(ind, pos, htf=None):
    """TSI cross above signal in positive territory = long; below in negative = short."""
    if pos < 1:
        return None
    t0 = ind["tsi"][pos]
    ts0 = ind["tsi_sig"][pos]
    t1 = ind["tsi"][pos - 1]
    ts1 = ind["tsi_sig"][pos - 1]
    if nan(t0, ts0, t1, ts1):
        return None

    if _xup(t0, t1, ts0, ts1) and t0 > 0:
        return "long"
    if _xdn(t0, t1, ts0, ts1) and t0 < 0:
        return "short"

    return None
