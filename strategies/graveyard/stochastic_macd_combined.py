#!/usr/bin/env python3
"""stochastic_macd_combined -- Stochastic K-D and MACD both must agree. Nikhil-Adithyan.

MACD above signal AND stoch_k above stoch_d simultaneously for entry.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "stochastic_macd_combined",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig, stoch_k, stoch_d",
    "long": "MACD > macd_sig AND stoch_k > stoch_d",
    "short": "MACD < macd_sig AND stoch_k < stoch_d",
    "desc": "Stochastic K-D and MACD dual confirmation entry",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python STOCH_MACD.py",
}


def signal(ind, pos, htf=None):
    """MACD and stochastic K-D both must agree."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    k = ind["stoch_k"][pos]
    d = ind["stoch_d"][pos]
    if nan(m, ms, k, d):
        return None
    if m > ms and k > d:
        return "long"
    if m < ms and k < d:
        return "short"
    return None
