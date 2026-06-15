#!/usr/bin/env python3
"""bollinger_band_mean_reversion -- BB touch + RSI oversold + Stoch cross mean reversion. web:forexfactory."""
from strategies._common import nan, REVERT, ALL_CLASSES, _xup, _xdn

META = {
    "id": "bollinger_band_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "bb_lo, bb_up, rsi, stoch_k, stoch_d, close",
    "long": "close touches bb_lo, rsi < 40, stoch_k < 20 and crossing above stoch_d",
    "short": "close touches bb_up, rsi > 60, stoch_k > 80 and crossing below stoch_d",
    "desc": "Bollinger Band bounce with RSI oversold/overbought and Stochastic cross confirmation",
    "source": "web:https://www.forexfactory.com/thread/2938-bollinger-bands-strategy",
}


def signal(ind, pos, htf=None):
    """BB mean reversion with RSI and Stochastic confirmation."""
    c = ind["close"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    rsi = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(c, bb_lo, bb_up, rsi, sk, sd, sk1, sd1):
        return None
    if c <= bb_lo and rsi < 40 and sk < 20 and _xup(sk, sk1, sd, sd1):
        return "long"
    if c >= bb_up and rsi > 60 and sk > 80 and _xdn(sk, sk1, sd, sd1):
        return "short"
    return None
