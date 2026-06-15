#!/usr/bin/env python3
"""tsi_true_strength_trend -- TSI signal-line cross with zero-line regime filter. web:chartschool.stockcharts.com.

TSI crosses above its signal line with TSI above zero = long. Below signal line + below
zero = short. Blau double-smoothed momentum oscillator trend system.
No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "tsi_true_strength_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "tsi, tsi_sig",
    "long": "tsi crosses above tsi_sig AND tsi > 0",
    "short": "tsi crosses below tsi_sig AND tsi < 0",
    "desc": "TSI True Strength Index signal-line cross with zero-line regime filter",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/true-strength-index",
}


def signal(ind, pos, htf=None):
    """TSI signal-line cross in the correct zero-line regime."""
    t, tp = ind["tsi"][pos], ind["tsi"][pos - 1]
    ts, tsp = ind["tsi_sig"][pos], ind["tsi_sig"][pos - 1]
    if nan(t, tp, ts, tsp):
        return None
    if _xup(t, tp, ts, tsp) and t > 0:
        return "long"
    if _xdn(t, tp, ts, tsp) and t < 0:
        return "short"
    return None
