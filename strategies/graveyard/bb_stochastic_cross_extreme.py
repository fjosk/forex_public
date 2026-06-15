#!/usr/bin/env python3
"""bb_stochastic_cross_extreme -- Stochastic crosses extreme level simultaneous with BB band touch. Nikhil-Adithyan."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_stochastic_cross_extreme",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "stoch_k, stoch_d, bb_lo, bb_up, close",
    "long": "stoch_k and stoch_d both cross below 30 AND close < bb_lo",
    "short": "stoch_k and stoch_d both cross above 70 AND close > bb_up",
    "desc": "BB band touch with simultaneous stochastic extreme crossover confirmation",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """Stoch cross of 30/70 level simultaneous with BB lower/upper touch."""
    stk = ind["stoch_k"][pos]
    std = ind["stoch_d"][pos]
    stk1 = ind["stoch_k"][pos - 1]
    std1 = ind["stoch_d"][pos - 1]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    c = ind["close"][pos]
    if nan(stk, std, stk1, std1, bb_lo, bb_up, c):
        return None
    # Both K and D cross below 30 and price below lower band
    if stk1 > 30 and std1 > 30 and stk < 30 and std < 30 and c < bb_lo:
        return "long"
    # Both K and D cross above 70 and price above upper band
    if stk1 < 70 and std1 < 70 and stk > 70 and std > 70 and c > bb_up:
        return "short"
    return None
