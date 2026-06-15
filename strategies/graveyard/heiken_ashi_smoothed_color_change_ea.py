#!/usr/bin/env python3
"""heiken_ashi_smoothed_color_change_ea -- HA color change with SMA20 trend filter. quivofx."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heiken_ashi_smoothed_color_change_ea",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, sma20, close",
    "long": "HA changes from bearish to bullish AND close > sma20",
    "short": "HA changes from bullish to bearish AND close < sma20",
    "desc": "Heiken-Ashi smoothed color change EA with SMA20 trend direction filter",
    "source": "https://quivofx.com/expert-advisor/heiken-ashi-smoothed-ea/",
}


def signal(ind, pos, htf=None):
    """HA color change with SMA20 trend filter."""
    hc = ind["ha_close"][pos]
    ho = ind["ha_open"][pos]
    hc1 = ind["ha_close"][pos - 1]
    ho1 = ind["ha_open"][pos - 1]
    s20 = ind["sma20"][pos]
    c = ind["close"][pos]
    if nan(hc, ho, hc1, ho1, s20, c):
        return None
    was_bear = hc1 < ho1
    now_bull = hc > ho
    was_bull = hc1 > ho1
    now_bear = hc < ho
    if was_bear and now_bull and c > s20:
        return "long"
    if was_bull and now_bear and c < s20:
        return "short"
    return None
