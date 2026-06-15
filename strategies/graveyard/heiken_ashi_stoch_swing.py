#!/usr/bin/env python3
"""heiken_ashi_stoch_swing -- HA color flip with Stochastic cross confirmation. web:https://www.forexfactory.com/thread/340556-swing-trading-with-heiken-ashi-and-stochs"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "heiken_ashi_stoch_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_open, ha_close, stoch_k, stoch_d",
    "long": "HA flips green from red AND stoch_k crosses above stoch_d below 50",
    "short": "HA flips red from green AND stoch_k crosses below stoch_d above 50",
    "desc": "Heikin Ashi color flip swing with Stochastic crossover timing",
    "source": "web:https://www.forexfactory.com/thread/340556-swing-trading-with-heiken-ashi-and-stochs",
}


def signal(ind, pos, htf=None):
    """HA color-change entry timed by stochastic crossover."""
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    hac1 = ind["ha_close"][pos - 1]
    hao1 = ind["ha_open"][pos - 1]
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(hac, hao, hac1, hao1, sk, sd, sk1, sd1):
        return None
    ha_bull = hac > hao
    ha_was_bear = hac1 < hao1
    ha_bear = hac < hao
    ha_was_bull = hac1 > hao1
    stoch_cross_up = _xup(sk, sk1, sd, sd1)
    stoch_cross_dn = _xdn(sk, sk1, sd, sd1)
    if ha_bull and ha_was_bear and stoch_cross_up and sk < 50:
        return "long"
    if ha_bear and ha_was_bull and stoch_cross_dn and sk > 50:
        return "short"
    return None
