#!/usr/bin/env python3
"""single_asset_6m_12m_momentum -- 6m and 12m return momentum (Robot Wealth / AQR). Both positive = long.

Buy when both 6-month (125 bars) and 12-month (252 bars) returns are positive.
Short when both are negative. Flat otherwise. Monthly rebalance gated by day-of-month.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "single_asset_6m_12m_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "close (6m/12m lookback), open_time (monthly gate)",
    "long": "6-month AND 12-month return both positive",
    "short": "6-month AND 12-month return both negative",
    "desc": "Single-asset 6- and 12-month absolute momentum (TSMOM single-instrument, Robot Wealth)",
    "source": "web:https://robotwealth.com/momentum-dead-alive/; AQR Asness/Moskowitz/Pedersen (2013)",
}

_LOOKBACK_6M = 125   # ~6 months of daily bars
_LOOKBACK_12M = 252  # ~12 months of daily bars


def signal(ind, pos, htf=None):
    """Dual-lookback absolute momentum signal, monthly rebalance gate."""
    if pos < _LOOKBACK_12M + 1:
        return None
    c = ind["close"][pos]
    c6 = ind["close"][pos - _LOOKBACK_6M]
    c12 = ind["close"][pos - _LOOKBACK_12M]
    ot = ind["open_time"][pos]
    if nan(c, c6, c12, ot):
        return None
    # monthly gate: only re-evaluate on first bar of each month
    # open_time is epoch ms; check that prior bar was a different calendar month
    ot_prev = ind["open_time"][pos - 1]
    if nan(ot_prev):
        return None
    # convert ms to day of month using integer arithmetic (ms -> days -> day-of-month)
    days_now = int(ot) // 86400000
    days_prev = int(ot_prev) // 86400000
    # approximate month boundary: day number % 31 resets; use 28-day minimum month
    # simple approach: only signal when crossing a ~30-day boundary
    if (days_now // 30) == (days_prev // 30):
        return None  # not a new month, hold current position
    ret_6m = (c - c6) / c6 if c6 != 0 else 0.0
    ret_12m = (c - c12) / c12 if c12 != 0 else 0.0
    if ret_6m > 0 and ret_12m > 0:
        return "long"
    if ret_6m < 0 and ret_12m < 0:
        return "short"
    return None
