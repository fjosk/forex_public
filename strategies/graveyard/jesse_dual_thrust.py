#!/usr/bin/env python3
"""jesse_dual_thrust -- Intraday volatility-adaptive dual-thrust breakout. Jesse AI example."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "jesse_dual_thrust",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hh_n, ll_n, close, high, low, atr",
    "long": "close breaks above anchor_close + 0.5 * range_up",
    "short": "close breaks below anchor_close - 0.5 * range_dn",
    "desc": "D.E. Shaw Dual Thrust: volatility-adaptive thrust levels from 21-bar range",
    "source": "web:https://github.com/jesse-ai/example-strategies/blob/master/DUAL_THRUST/__init__.py",
}

_N = 21
_COEFF = 0.5


def signal(ind, pos, htf=None):
    """Dual thrust: compute range_up/dn over last N bars and compare to thrust levels."""
    c = ind["close"][pos]
    if nan(c):
        return None
    if pos < _N + 1:
        return None
    # Compute thrust range from the prior N bars
    max_close = max_high = float("-inf")
    min_close = min_low = float("inf")
    for i in range(pos - _N, pos):
        cl_i = ind["close"][i]
        hi_i = ind["high"][i]
        lo_i = ind["low"][i]
        if nan(cl_i, hi_i, lo_i):
            return None
        max_close = max(max_close, cl_i)
        min_close = min(min_close, cl_i)
        max_high = max(max_high, hi_i)
        min_low = min(min_low, lo_i)
    range_up = max(max_close - min_low, max_high - min_close)
    range_dn = range_up
    anchor_close = ind["close"][pos - 1]
    if nan(anchor_close):
        return None
    up_thrust = anchor_close + _COEFF * range_up
    dn_thrust = anchor_close - _COEFF * range_dn
    if c > up_thrust:
        return "long"
    if c < dn_thrust:
        return "short"
    return None
