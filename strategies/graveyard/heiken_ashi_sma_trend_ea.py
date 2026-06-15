#!/usr/bin/env python3
"""heiken_ashi_sma_trend_ea -- HA color change + SMA trend filter. MQL5 code base EA."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heiken_ashi_sma_trend_ea",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, sma20, close",
    "long": "HA just turned bullish (prior bar was bearish) AND close > sma20",
    "short": "HA just turned bearish (prior bar was bullish) AND close < sma20",
    "desc": "Heiken Ashi + SMA trend EA: enter on HA color flip confirmed by SMA position",
    "source": "web:https://www.mql5.com/en/code/mt4/experts/page12",
}


def signal(ind, pos, htf=None):
    """HA color flip entry with SMA trend confirmation."""
    ha_c = ind["ha_close"][pos]
    ha_o = ind["ha_open"][pos]
    ha_c1 = ind["ha_close"][pos - 1]
    ha_o1 = ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    sma = ind["sma20"][pos]
    if nan(ha_c, ha_o, ha_c1, ha_o1, c, sma):
        return None
    ha_bull = ha_c > ha_o
    ha_bear = ha_c < ha_o
    was_bull = ha_c1 > ha_o1
    was_bear = ha_c1 < ha_o1
    if ha_bull and was_bear and c > sma:
        return "long"
    if ha_bear and was_bull and c < sma:
        return "short"
    return None
