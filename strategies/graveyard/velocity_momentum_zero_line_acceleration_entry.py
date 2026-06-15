#!/usr/bin/env python3
"""velocity_momentum_zero_line_acceleration_entry -- ROC crosses above zero AND ROC is accelerating upward (ROC[i] > ROC[i-1]). Trade Your Way to Financial Freedom.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "velocity_momentum_zero_line_acceleration_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "roc",
    "long": "ROC crosses above zero AND ROC accelerating up (ROC[i] > ROC[i-1])",
    "short": "ROC crosses below zero AND ROC accelerating down (ROC[i] < ROC[i-1])",
    "desc": "Speed zero-cross with acceleration confirmation: velocity turns positive AND gaining speed",
    "source": "Trade Your Way to Financial Freedom, Ch.8 Designing Your Own Entry Signal (speed/velocity/acceleration)",
}


def signal(ind, pos, htf=None):
    """ROC zero-cross with acceleration confirmation."""
    if pos < 1:
        return None
    r = ind["roc"][pos]
    r1 = ind["roc"][pos - 1]
    if nan(r, r1):
        return None
    a = r - r1
    if _xup(r, r1, 0.0, 0.0) and a > 0:
        return "long"
    if _xdn(r, r1, 0.0, 0.0) and a < 0:
        return "short"
    return None
