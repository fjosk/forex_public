#!/usr/bin/env python3
"""ema9_21_stoch_5m_pullback -- EMA9/21 trend + stochastic oversold/overbought cross entry. web:forextraders.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema9_21_stoch_5m_pullback",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema9, ema21, stoch_k",
    "long": "ema9 > ema21 AND stoch_k crosses above 20",
    "short": "ema9 < ema21 AND stoch_k crosses below 80",
    "desc": "EMA9/21 trend with stochastic pullback cross entry scalp",
    "source": "web:https://forextraders.com/forex-education/forex-scalping/simple-1-5-and-15-minute-forex-scalping-strategies/",
}


def signal(ind, pos, htf=None):
    """EMA alignment confirms trend; stoch cross from oversold/overbought times the entry."""
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    if nan(e9, e21, stk, stk_p):
        return None
    if e9 > e21 and stk > 20 and stk_p <= 20:
        return "long"
    if e9 < e21 and stk < 80 and stk_p >= 80:
        return "short"
    return None
