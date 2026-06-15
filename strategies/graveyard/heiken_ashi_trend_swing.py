#!/usr/bin/env python3
"""heiken_ashi_trend_swing -- Heikin Ashi trend swing: first green HA after red series above SMA100. web:theforexgeek.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "heiken_ashi_trend_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ha_close, ha_open, sma100, close",
    "long": "close above sma100, prior HA bar was red, current HA bar is green",
    "short": "close below sma100, prior HA bar was green, current HA bar is red",
    "desc": "Heikin Ashi trend: first HA reversal candle after corrective series with SMA100 filter",
    "source": "web:https://theforexgeek.com/swing-trading-with-heikin-ashi-strategy/",
}


def signal(ind, pos, htf=None):
    """First green/red HA candle after prior red/green series, filtered by SMA100."""
    hac, hao = ind["ha_close"][pos], ind["ha_open"][pos]
    hac1, hao1 = ind["ha_close"][pos - 1], ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    sma = ind["sma100"][pos]
    if nan(hac, hao, hac1, hao1, c, sma):
        return None
    ha_green = hac > hao
    ha_red = hac < hao
    prev_red = hac1 < hao1
    prev_green = hac1 > hao1
    if c > sma and ha_green and prev_red:
        return "long"
    if c < sma and ha_red and prev_green:
        return "short"
    return None
