#!/usr/bin/env python3
"""heikin_ashi_supertrend -- HA color flip with SuperTrend direction filter. web:https://www.tradingview.com/script/9z16eauD-Heikin-Ashi-Supertrend/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heikin_ashi_supertrend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, st_dir, ema200, close",
    "long": "HA flips green (from red) AND st_dir == 1 AND close > ema200",
    "short": "HA flips red (from green) AND st_dir == -1 AND close < ema200",
    "desc": "Heikin Ashi color flip confirmed by SuperTrend direction and EMA200 filter",
    "source": "web:https://www.tradingview.com/script/9z16eauD-Heikin-Ashi-Supertrend/",
}


def signal(ind, pos, htf=None):
    """HA color flip with st_dir and EMA200 macro filter."""
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    hac1 = ind["ha_close"][pos - 1]
    hao1 = ind["ha_open"][pos - 1]
    st = ind["st_dir"][pos]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(hac, hao, hac1, hao1, st, c, e200):
        return None
    ha_bull = hac > hao
    ha_was_bull = hac1 > hao1
    ha_bull_flip = ha_bull and not ha_was_bull
    ha_bear_flip = (not ha_bull) and ha_was_bull
    if ha_bull_flip and st == 1 and c > e200:
        return "long"
    if ha_bear_flip and st == -1 and c < e200:
        return "short"
    return None
