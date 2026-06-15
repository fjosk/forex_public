#!/usr/bin/env python3
"""sma25_sma50_stoch_1m -- SMA20/50 trend alignment + stochastic oversold/overbought cross. web:forextraders.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sma25_sma50_stoch_1m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "sma20 (proxy sma25), sma50, stoch_k",
    "long": "sma20 > sma50 (uptrend) AND stoch_k crosses above 20",
    "short": "sma20 < sma50 (downtrend) AND stoch_k crosses below 80",
    "desc": "SMA25/50 trend alignment with stochastic oversold/overbought pullback entry scalp",
    "source": "web:https://forextraders.com/forex-education/forex-scalping/simple-1-5-and-15-minute-forex-scalping-strategies/",
}


def signal(ind, pos, htf=None):
    """SMA alignment defines trend; stochastic cross from extreme level times the pullback entry."""
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    if nan(s20, s50, stk, stk_p):
        return None
    if s20 > s50 and stk > 20 and stk_p <= 20:
        return "long"
    if s20 < s50 and stk < 80 and stk_p >= 80:
        return "short"
    return None
