#!/usr/bin/env python3
"""sma5_10_stoch_rsi_swing -- SMA5/10 cross + Stochastic extreme + RSI50. web:forexmt4indicators.com.

Three-indicator confluence: fast/slow SMA crossover for trend, stochastic exiting an
extreme zone for timing, RSI above/below 50 for momentum confirmation.
No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "sma5_10_stoch_rsi_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema5, sma10, stoch_k, rsi",
    "long": "ema5 crosses above sma10 AND stoch_k < 20 hooking up AND rsi >= 50",
    "short": "ema5 crosses below sma10 AND stoch_k > 80 hooking down AND rsi <= 50",
    "desc": "SMA5/10 cross with Stochastic extreme exit and RSI50 confirmation",
    "source": "web:https://forexmt4indicators.com/sma-stochastic-rsi-forex-swing-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """SMA cross + stochastic extreme hook + RSI regime."""
    e5, e5p = ind["ema5"][pos], ind["ema5"][pos - 1]
    s10, s10p = ind["sma10"][pos], ind["sma10"][pos - 1]
    sk, skp = ind["stoch_k"][pos], ind["stoch_k"][pos - 1]
    r = ind["rsi"][pos]
    if nan(e5, e5p, s10, s10p, sk, skp, r):
        return None
    cross_up = _xup(e5, e5p, s10, s10p)
    cross_dn = _xdn(e5, e5p, s10, s10p)
    stoch_hook_up = sk < 20 and sk > skp
    stoch_hook_dn = sk > 80 and sk < skp
    if cross_up and stoch_hook_up and r >= 50:
        return "long"
    if cross_dn and stoch_hook_dn and r <= 50:
        return "short"
    return None
