#!/usr/bin/env python3
"""velocity_acceleration_first_and_second_differences_reversal -- Velocity (close diff) zero-cross confirmed by acceleration (2nd diff) direction. Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "velocity_acceleration_first_and_second_differences_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Velocity (close - close[1]) crosses above 0 AND acceleration > 0",
    "short": "Velocity crosses below 0 AND acceleration < 0",
    "desc": "Kaufman velocity/acceleration first and second differences: velocity zero-cross plus acceleration confirmation",
    "source": "Kaufman, Trading Systems and Methods, Ch6 Velocity and Acceleration, p.149-152",
}


def signal(ind, pos, htf=None):
    """Velocity zero-cross with acceleration confirmation."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    if nan(c, c1, c2):
        return None
    v = c - c1
    v1 = c1 - c2
    a = v - v1
    if _xup(v, v1, 0.0, 0.0) and a > 0:
        return "long"
    if _xdn(v, v1, 0.0, 0.0) and a < 0:
        return "short"
    return None
