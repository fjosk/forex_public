#!/usr/bin/env python3
"""macd_crossover_trend_filter -- MACD signal-line cross below/above zero filtered by SMA200. arXiv 2206.12282.

Long: MACD crosses above signal while MACD < 0 and close > SMA200.
Short: MACD crosses below signal while MACD > 0 and close < SMA200.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_crossover_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "macd, macd_sig, sma200",
    "long": "MACD crosses above signal while MACD < 0 and close > SMA200",
    "short": "MACD crosses below signal while MACD > 0 and close < SMA200",
    "desc": "MACD signal-line crossover below/above zero with SMA200 trend filter",
    "source": "web:https://arxiv.org/pdf/2206.12282",
}


def signal(ind, pos, htf=None):
    """MACD cross with zero-line and SMA200 filter."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(m, ms, m1, ms1, s200, c):
        return None
    bull_cross = _xup(m, m1, ms, ms1)
    bear_cross = _xdn(m, m1, ms, ms1)
    if bull_cross and m < 0 and c > s200:
        return "long"
    if bear_cross and m > 0 and c < s200:
        return "short"
    return None
