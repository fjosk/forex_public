#!/usr/bin/env python3
"""velocity_acceleration_trend_change_detector_first_second_differences -- Velocity (first diff) zero-cross as trend change detector; acceleration (second diff) as leading signal. Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "velocity_acceleration_trend_change_detector_first_second_differences",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Velocity (close - close[1]) crosses above 0 (uptrend start)",
    "short": "Velocity crosses below 0 (downtrend start)",
    "desc": "Kaufman velocity/acceleration trend change: velocity sign cross signals trend turn",
    "source": "Kaufman, Trading Systems and Methods, Ch6 Velocity and Acceleration Quick Calculation, p.151-152",
}


def signal(ind, pos, htf=None):
    """Velocity zero-cross as trend change signal."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c, c1):
        return None
    if pos < 2:
        return None
    c2 = ind["close"][pos - 2]
    if nan(c2):
        return None
    v = c - c1
    v1 = c1 - c2
    if _xup(v, v1, 0.0, 0.0):
        return "long"
    if _xdn(v, v1, 0.0, 0.0):
        return "short"
    return None
