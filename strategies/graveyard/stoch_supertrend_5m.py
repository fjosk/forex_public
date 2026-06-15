#!/usr/bin/env python3
"""stoch_supertrend_5m -- SuperTrend direction + Stochastic OB/OS 5m scalp.

Long:  price above SuperTrend (st_dir > 0) AND stoch_k touches or goes below 20.
Short: price below SuperTrend (st_dir < 0) AND stoch_k touches or goes above 80.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stoch_supertrend_5m",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "st_dir, st_line, stoch_k, stoch_d",
    "long": "st_dir > 0 (price above SuperTrend) AND stoch_k <= 20 (oversold pullback)",
    "short": "st_dir < 0 (price below SuperTrend) AND stoch_k >= 80 (overbought pullback)",
    "desc": "SuperTrend trend direction + Stochastic oversold/overbought 5m scalp",
    "source": "web:https://forextradingstrategies4u.com/5-minute-forex-scalping-system-with-stochastic-and-supertrend-indicator/",
}


def signal(ind, pos, htf=None):
    """SuperTrend + Stochastic 5m scalp."""
    st = ind["st_dir"][pos]
    sk = ind["stoch_k"][pos]
    c = ind["close"][pos]
    if nan(st, sk, c):
        return None
    if st > 0 and sk <= 20:
        return "long"
    if st < 0 and sk >= 80:
        return "short"
    return None
