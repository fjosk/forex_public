#!/usr/bin/env python3
"""heikin_ashi_trend_direction -- Standard candle closes above/below prior HA open of opposite color. hasnocool."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heikin_ashi_trend_direction",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, close, open",
    "long": "prev HA bearish AND current candle: close > open AND close > prev ha_open",
    "short": "prev HA bullish AND current candle: close < open AND close < prev ha_open",
    "desc": "Heikin-Ashi trend direction change: standard candle breakout above/below prior HA open",
    "source": "https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Heikin%20Ashi%20Trend%20Direction%20Strategy.pine",
}


def signal(ind, pos, htf=None):
    """HA direction change via standard candle close vs prior HA open."""
    hc1 = ind["ha_close"][pos - 1]
    ho1 = ind["ha_open"][pos - 1]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(hc1, ho1, c, o):
        return None
    prev_bear = hc1 < ho1
    prev_bull = hc1 > ho1
    if prev_bear and c > o and c > ho1:
        return "long"
    if prev_bull and c < o and c < ho1:
        return "short"
    return None
