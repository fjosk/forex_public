#!/usr/bin/env python3
"""heiken_ashi_color_flip -- First bullish HA after bearish = long; first bearish after bullish = short. mql5."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heiken_ashi_color_flip",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ha_close, ha_open",
    "long": "current HA bullish (ha_close > ha_open) AND previous HA was bearish",
    "short": "current HA bearish AND previous HA was bullish",
    "desc": "Heiken-Ashi color flip: enter on first candle of new color",
    "source": "https://www.mql5.com/en/articles/91",
}


def signal(ind, pos, htf=None):
    """HA color flip entry."""
    hc = ind["ha_close"][pos]
    ho = ind["ha_open"][pos]
    hc1 = ind["ha_close"][pos - 1]
    ho1 = ind["ha_open"][pos - 1]
    if nan(hc, ho, hc1, ho1):
        return None
    ha_bull = hc > ho
    ha_bear = hc < ho
    prev_bull = hc1 > ho1
    prev_bear = hc1 < ho1
    if ha_bull and prev_bear:
        return "long"
    if ha_bear and prev_bull:
        return "short"
    return None
