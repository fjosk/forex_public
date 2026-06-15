#!/usr/bin/env python3
"""qqe_rsi_smoothed_cross -- QQE smoothed RSI crosses its ATR band with 50-level bias. edyatl/qqe-mod.

qqe_line crosses qqe_rsima AND directional bias from the 50-level.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "qqe_rsi_smoothed_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "qqe_line, qqe_rsima",
    "long": "qqe_line crosses above qqe_rsima AND qqe_line > 50",
    "short": "qqe_line crosses below qqe_rsima AND qqe_line < 50",
    "desc": "QQE smoothed RSI cross with 50-level directional bias",
    "source": "https://github.com/edyatl/qqe-mod",
}


def signal(ind, pos, htf=None):
    """QQE line vs RSI MA cross with 50-level bias filter."""
    q = ind["qqe_line"][pos]
    q1 = ind["qqe_line"][pos - 1]
    r = ind["qqe_rsima"][pos]
    r1 = ind["qqe_rsima"][pos - 1]
    if nan(q, q1, r, r1):
        return None
    if _xup(q, q1, r, r1) and q > 50:
        return "long"
    if _xdn(q, q1, r, r1) and q < 50:
        return "short"
    return None
