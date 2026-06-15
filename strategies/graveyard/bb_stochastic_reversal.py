#!/usr/bin/env python3
"""bb_stochastic_reversal -- Bollinger Band + Stochastic Reversal. Nikhil-Adithyan BB_STOCH.py."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_stochastic_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, stoch_k",
    "long": "close < bb_lo AND stoch_k < 20",
    "short": "close > bb_up AND stoch_k > 80",
    "desc": "Price at BB extreme confirmed by Stochastic overbought/oversold alignment",
    "source": "github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """BB extreme + stochastic oversold/overbought confirmation."""
    c = ind["close"][pos]
    bbl = ind["bb_lo"][pos]
    bbu = ind["bb_up"][pos]
    sk = ind["stoch_k"][pos]
    if nan(c, bbl, bbu, sk):
        return None
    if c < bbl and sk < 20:
        return "long"
    if c > bbu and sk > 80:
        return "short"
    return None
