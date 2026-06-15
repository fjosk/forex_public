#!/usr/bin/env python3
"""heikin_ashi_ema_trend -- HA color flip with EMA9/21 alignment. web:https://www.quantifiedstrategies.com/heikin-ashi-trading-strategy/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heikin_ashi_ema_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, ema9, ema21",
    "long": "ema9 > ema21, ha_close > ema9 and ema21, HA color flips green",
    "short": "ema9 < ema21, ha_close < ema9 and ema21, HA color flips red",
    "desc": "Heikin Ashi color flip confirmed by EMA9/21 alignment and HA position",
    "source": "web:https://www.quantifiedstrategies.com/heikin-ashi-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """HA color flip when aligned with EMA9/21 trend and HA above/below both EMAs."""
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    hac1 = ind["ha_close"][pos - 1]
    hao1 = ind["ha_open"][pos - 1]
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    if nan(hac, hao, hac1, hao1, e9, e21):
        return None
    bull_ema = e9 > e21
    bear_ema = e9 < e21
    ha_bull_bar = hac > hao
    ha_bear_bar = hac < hao
    ha_bull_prev = hac1 > hao1
    ha_bull_flip = ha_bull_bar and not ha_bull_prev
    ha_bear_flip = ha_bear_bar and not ha_bull_prev
    if bull_ema and ha_bull_flip and hac > e9 and hac > e21:
        return "long"
    if bear_ema and ha_bear_flip and hac < e9 and hac < e21:
        return "short"
    return None
