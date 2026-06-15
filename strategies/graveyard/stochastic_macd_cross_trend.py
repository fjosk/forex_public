#!/usr/bin/env python3
"""stochastic_macd_cross_trend -- Stochastic K>D + MACD>signal dual confirmation. armelf Financial-Algorithms.

Both oscillators must agree: K above D AND MACD above signal = long.
K below D AND MACD below signal = short.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "stochastic_macd_cross_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "stoch_k, stoch_d, macd, macd_sig",
    "long": "stoch_k > stoch_d AND macd > macd_sig",
    "short": "stoch_k < stoch_d AND macd < macd_sig",
    "desc": "Stochastic K/D + MACD/signal dual oscillator cross confirmation",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """Both stochastic and MACD agree on direction."""
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    if nan(sk, sd, m, ms):
        return None
    if sk > sd and m > ms:
        return "long"
    if sk < sd and m < ms:
        return "short"
    return None
