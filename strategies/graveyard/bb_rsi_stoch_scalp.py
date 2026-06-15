#!/usr/bin/env python3
"""bb_rsi_stoch_scalp -- BB + RSI + Stochastic triple-confirmation mean-reversion scalp. web:forextester."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_rsi_stoch_scalp",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "bb_lo, bb_up, rsi, stoch_k",
    "long": "close <= bb_lo AND rsi < 30 AND stoch_k < 20",
    "short": "close >= bb_up AND rsi > 70 AND stoch_k > 80",
    "desc": "Triple-confirmation extreme reversal scalp: BB pierce + RSI extreme + Stoch extreme",
    "source": "web:https://forextester.com/blog/bollinger-bands-rsi-stochastic-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """BB + RSI + Stochastic triple-confirmation scalp."""
    c = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    rsi = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    if nan(c, bb_up, bb_lo, rsi, sk):
        return None
    if c <= bb_lo and rsi < 30 and sk < 20:
        return "long"
    if c >= bb_up and rsi > 70 and sk > 80:
        return "short"
    return None
