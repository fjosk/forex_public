#!/usr/bin/env python3
"""time_series_momentum_tsmom -- 12-month absolute return momentum, monthly rebalance. Moskowitz/Ooi/Pedersen (2012).

Go long if 12-month return (close vs close 252 bars ago) is positive; short if negative.
Monthly rebalance gate. Volatility scaling is a sizing concern; this module returns direction only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "time_series_momentum_tsmom",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "close (252-bar lookback), open_time (monthly gate)",
    "long": "12-month return positive (close > close 252 bars ago)",
    "short": "12-month return negative",
    "desc": "TSMOM 12-month time-series momentum, monthly rebalance (Moskowitz et al 2012)",
    "source": "web:https://quantpedia.com/strategies/time-series-momentum-effect; SSRN 2089463",
}

_LOOKBACK = 252


def signal(ind, pos, htf=None):
    """TSMOM: sign of 12-month return, monthly gate."""
    if pos < _LOOKBACK + 1:
        return None
    c = ind["close"][pos]
    c_prev = ind["close"][pos - _LOOKBACK]
    ot = ind["open_time"][pos]
    ot_prev = ind["open_time"][pos - 1]
    if nan(c, c_prev, ot, ot_prev):
        return None
    # monthly gate
    days_now = int(ot) // 86400000
    days_prev = int(ot_prev) // 86400000
    if (days_now // 30) == (days_prev // 30):
        return None
    ret = (c - c_prev) / c_prev if c_prev != 0 else 0.0
    if ret > 0:
        return "long"
    if ret < 0:
        return "short"
    return None
