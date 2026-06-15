#!/usr/bin/env python3
"""heikin_ashi_color_change_ema -- Heikin Ashi color change entry with EMA200 trend filter. blog.opofinance.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "heikin_ashi_color_change_ema",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, ema200",
    "long": "HA flips from red to green (ha_close > ha_open after ha_close < ha_open) AND close > ema200",
    "short": "HA flips from green to red AND close < ema200",
    "desc": "Heikin Ashi color change (red->green or green->red) with EMA200 trend direction filter",
    "source": "web:https://blog.opofinance.com/en/heikin-ashi-strategy/",
}


def signal(ind, pos, htf=None):
    """Heikin Ashi color flip with EMA200 trend gate."""
    hc = ind["ha_close"][pos]
    ho = ind["ha_open"][pos]
    hcp = ind["ha_close"][pos - 1]
    hop = ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(hc, ho, hcp, hop, c, e200):
        return None
    ha_bull = hc > ho
    ha_bear = hc < ho
    ha_bull_prev = hcp > hop
    ha_bear_prev = hcp < hop
    # Color change from red to green
    flip_bull = ha_bull and ha_bear_prev
    # Color change from green to red
    flip_bear = ha_bear and ha_bull_prev
    if flip_bull and c > e200:
        return "long"
    if flip_bear and c < e200:
        return "short"
    return None
