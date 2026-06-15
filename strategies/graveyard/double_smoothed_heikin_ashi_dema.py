#!/usr/bin/env python3
"""double_smoothed_heikin_ashi_dema -- HA color flip with EMA200 regime filter. web:https://medium.com/@redsword_23261/double-smoothed-heiken-ashi-trend-following-strategy-ce4695347376"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "double_smoothed_heikin_ashi_dema",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, ema200",
    "long": "HA flips green (ha_close > ha_open) after red bar AND close above ema200",
    "short": "HA flips red after green bar AND close below ema200",
    "desc": "Double-smoothed Heikin Ashi color flip with EMA200 trend filter",
    "source": "web:https://medium.com/@redsword_23261/double-smoothed-heiken-ashi-trend-following-strategy-ce4695347376",
}


def signal(ind, pos, htf=None):
    """HA color flip filtered by EMA200 regime."""
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    hac1 = ind["ha_close"][pos - 1]
    hao1 = ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(hac, hao, hac1, hao1, c, e200):
        return None
    ha_green = hac > hao
    ha_was_red = hac1 < hao1
    ha_red = hac < hao
    ha_was_green = hac1 > hao1
    if ha_green and ha_was_red and c > e200:
        return "long"
    if ha_red and ha_was_green and c < e200:
        return "short"
    return None
