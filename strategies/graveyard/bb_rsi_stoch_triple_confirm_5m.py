#!/usr/bin/env python3
"""bb_rsi_stoch_triple_confirm_5m -- BB extreme + RSI < 30 + Stoch < 20 triple confirmation. web:forextester.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_rsi_stoch_triple_confirm_5m",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "bb_up, bb_lo, rsi, stoch_k",
    "long": "close < bb_lo AND rsi < 30 AND stoch_k < 20",
    "short": "close > bb_up AND rsi > 70 AND stoch_k > 80",
    "desc": "Triple-confirm BB mean reversion: band extreme + RSI extreme + Stochastic extreme",
    "source": "web:https://forextester.com/blog/bollinger-bands-rsi-stochastic-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """All three indicators confirm at the same bar before entry."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    rsi = ind["rsi"][pos]
    stk = ind["stoch_k"][pos]
    c = ind["close"][pos]
    if nan(bb_up, bb_lo, rsi, stk, c):
        return None
    if c < bb_lo and rsi < 30 and stk < 20:
        return "long"
    if c > bb_up and rsi > 70 and stk > 80:
        return "short"
    return None
