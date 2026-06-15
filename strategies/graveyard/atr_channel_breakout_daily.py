#!/usr/bin/env python3
"""atr_channel_breakout_daily -- ATR channel breakout around long SMA (Curtis Faith). web:whselfinvest."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "atr_channel_breakout_daily",
    "cadences": ["swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "1d",
    "indicators": "atr, sma200, close",
    "long": "close breaks above SMA200 + 7*ATR channel upper band",
    "short": "close breaks below SMA200 - 3*ATR channel lower band",
    "desc": "ATR channel breakout around 200-period SMA (proxy for Curtis Faith 350-SMA variant)",
    "source": "web:https://www.whselfinvest.com/en-lu/trading-platform_free-trading-strategies_tradingsystem_80-atr-channel-breakout-curtis-faith",
}

_MULT_UP = 7.0
_MULT_DN = 3.0


def signal(ind, pos, htf=None):
    """ATR channel breakout around SMA200."""
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    atr = ind["atr"][pos]
    if nan(c, s200, atr):
        return None
    upper_ch = s200 + _MULT_UP * atr
    lower_ch = s200 - _MULT_DN * atr
    if c > upper_ch:
        return "long"
    if c < lower_ch:
        return "short"
    return None
