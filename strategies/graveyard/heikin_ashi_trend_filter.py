#!/usr/bin/env python3
"""heikin_ashi_trend_filter -- HA candle direction + EMA20 trend confirmation. QuantConnect forum."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heikin_ashi_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ha_close, ha_open, ema20",
    "long": "ha_close > ha_open (bullish HA) AND close > ema20",
    "short": "ha_close < ha_open (bearish HA) AND close < ema20",
    "desc": "Heikin-Ashi trend filter with EMA20 trend confirmation",
    "source": "web:https://www.quantconnect.com/forum/discussion/10899/",
}


def signal(ind, pos, htf=None):
    """HA candle direction filtered by EMA20 trend."""
    ha_c = ind["ha_close"][pos]
    ha_o = ind["ha_open"][pos]
    ha_c1 = ind["ha_close"][pos - 1]
    ha_o1 = ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    ema20 = ind["ema20"][pos]
    if nan(ha_c, ha_o, ha_c1, ha_o1, c, ema20):
        return None
    ha_bull = ha_c > ha_o
    ha_bear = ha_c < ha_o
    was_bull = ha_c1 > ha_o1
    was_bear = ha_c1 < ha_o1
    # Enter long when HA just turns bullish and price above EMA20
    if ha_bull and was_bear and c > ema20:
        return "long"
    # Enter short when HA just turns bearish and price below EMA20
    if ha_bear and was_bull and c < ema20:
        return "short"
    return None
