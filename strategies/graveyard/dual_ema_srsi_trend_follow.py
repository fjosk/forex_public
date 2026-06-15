#!/usr/bin/env python3
"""dual_ema_srsi_trend_follow -- EMA9/21 crossover with Stochastic RSI pullback entry. web:https://medium.com/@redsword_23261/dual-ema-and-stochastic-rsi-trend-following-strategy-7da2bd78b743"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "dual_ema_srsi_trend_follow",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema9, ema21, srsi_k, srsi_d",
    "long": "ema9 > ema21 AND srsi_k crosses above srsi_d below 20",
    "short": "ema9 < ema21 AND srsi_k crosses below srsi_d above 80",
    "desc": "Dual EMA trend direction with Stochastic RSI pullback timing",
    "source": "web:https://medium.com/@redsword_23261/dual-ema-and-stochastic-rsi-trend-following-strategy-7da2bd78b743",
}


def signal(ind, pos, htf=None):
    """EMA9/21 trend filter with stochRSI oversold/overbought entry."""
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    sk = ind["srsi_k"][pos]
    sd = ind["srsi_d"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    sd1 = ind["srsi_d"][pos - 1]
    if nan(e9, e21, sk, sd, sk1, sd1):
        return None
    trend_up = e9 > e21
    trend_dn = e9 < e21
    srsi_cross_up = _xup(sk, sk1, sd, sd1)
    srsi_cross_dn = _xdn(sk, sk1, sd, sd1)
    if trend_up and srsi_cross_up and sk < 20:
        return "long"
    if trend_dn and srsi_cross_dn and sk > 80:
        return "short"
    return None
