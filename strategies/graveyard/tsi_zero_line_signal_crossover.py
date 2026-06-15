#!/usr/bin/env python3
"""tsi_zero_line_signal_crossover -- TSI signal-line crossover with zero-line directional filter. web:quantifiedstrategies.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "tsi_zero_line_signal_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "tsi, tsi_sig",
    "long": "TSI above zero and crosses above its signal line",
    "short": "TSI below zero and crosses below its signal line",
    "desc": "TSI signal-line crossover with zero-line directional filter",
    "source": "web:https://www.quantifiedstrategies.com/true-strength-index/",
}


def signal(ind, pos, htf=None):
    """TSI zero-line filter + signal-line crossover."""
    t, ts = ind["tsi"][pos], ind["tsi_sig"][pos]
    t1, ts1 = ind["tsi"][pos - 1], ind["tsi_sig"][pos - 1]
    if nan(t, ts, t1, ts1):
        return None
    if t > 0 and _xup(t, t1, ts, ts1):
        return "long"
    if t < 0 and _xdn(t, t1, ts, ts1):
        return "short"
    return None
