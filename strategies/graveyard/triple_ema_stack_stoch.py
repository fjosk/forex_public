#!/usr/bin/env python3
"""triple_ema_stack_stoch -- Triple EMA stack (50/100/200) + Stochastic extreme exit. web:earnforex.com.

Daily EMA50 > SMA100 > EMA200 perfect stack confirms direction. Stochastic K/D cross out
of extreme zone (below 10 for longs, above 90 for shorts) provides the entry trigger.
sma100 used as proxy for ema100 (not in indicator set). No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "triple_ema_stack_stoch",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema50, sma100 (proxy ema100), ema200, stoch_k, stoch_d, close",
    "long": "close > ema50 > sma100 > ema200 AND stoch_k crosses above stoch_d below 10",
    "short": "close < ema50 < sma100 < ema200 AND stoch_k crosses below stoch_d above 90",
    "desc": "Triple EMA 50/100/200 stack with Stochastic extreme-exit trigger",
    "source": "web:https://www.earnforex.com/forex-strategy/combined-stochastic-ma-strategy/",
}


def signal(ind, pos, htf=None):
    """EMA perfect stack + stochastic extreme cross entry."""
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    s100 = ind["sma100"][pos]
    e200 = ind["ema200"][pos]
    sk, skp = ind["stoch_k"][pos], ind["stoch_k"][pos - 1]
    sd, sdp = ind["stoch_d"][pos], ind["stoch_d"][pos - 1]
    if nan(c, e50, s100, e200, sk, skp, sd, sdp):
        return None
    stack_long = c > e50 > s100 > e200
    stack_short = c < e50 < s100 < e200
    # stochastic K/D cross from extreme zones
    stoch_cross_up = _xup(sk, skp, sd, sdp) and skp < 10
    stoch_cross_dn = _xdn(sk, skp, sd, sdp) and skp > 90
    if stack_long and stoch_cross_up:
        return "long"
    if stack_short and stoch_cross_dn:
        return "short"
    return None
