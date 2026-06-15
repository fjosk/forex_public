#!/usr/bin/env python3
"""stochastic_macd_trend_combo -- MACD and stochastic both directional state agree. armelf/Financial-Algorithms.

Both the MACD spread (above/below signal) and the stochastic K-D spread must point the same way.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "stochastic_macd_trend_combo",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "macd, macd_sig, stoch_k, stoch_d",
    "long": "MACD > macd_sig (MACD bullish spread) AND stoch_k > stoch_d (stoch bullish)",
    "short": "MACD < macd_sig AND stoch_k < stoch_d",
    "desc": "MACD and stochastic directional state dual confirm",
    "source": "https://github.com/armelf/Financial-Algorithms Stochastic MACD Strategy",
}


def signal(ind, pos, htf=None):
    """Both MACD and stochastic K-D spread must agree."""
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
