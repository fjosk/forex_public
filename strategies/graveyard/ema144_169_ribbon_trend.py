#!/usr/bin/env python3
"""ema144_169_ribbon_trend -- Fibonacci EMA 144/169 ribbon trend entry. web:https://comparic.com/trading-based-ema-144/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema144_169_ribbon_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema144, ema169, ema13, ema21",
    "long": "ema144 and ema169 rising, ema13 crosses above ema144/169 ribbon",
    "short": "ema144 and ema169 falling, ema13 crosses below ema144/169 ribbon",
    "desc": "Fibonacci EMA 144/169 ribbon trend with fast EMA breakout entry",
    "source": "web:https://comparic.com/trading-based-ema-144/",
}


def signal(ind, pos, htf=None):
    """Fast EMA13 crosses the 144/169 ribbon with ribbon-slope confirmation."""
    e13 = ind["ema13"][pos]
    e13_1 = ind["ema13"][pos - 1]
    e144 = ind["ema144"][pos]
    e144_1 = ind["ema144"][pos - 1]
    e169 = ind["ema169"][pos]
    e169_1 = ind["ema169"][pos - 1]
    if nan(e13, e13_1, e144, e144_1, e169, e169_1):
        return None
    ribbon_top = max(e144, e169)
    ribbon_bot = min(e144, e169)
    ribbon_top_1 = max(e144_1, e169_1)
    ribbon_bot_1 = min(e144_1, e169_1)
    ribbon_rising = e144 > e144_1 and e169 > e169_1
    ribbon_falling = e144 < e144_1 and e169 < e169_1
    # fast EMA crosses above ribbon top
    cross_above = e13 > ribbon_top and e13_1 <= ribbon_top_1
    # fast EMA crosses below ribbon bottom
    cross_below = e13 < ribbon_bot and e13_1 >= ribbon_bot_1
    if cross_above and ribbon_rising:
        return "long"
    if cross_below and ribbon_falling:
        return "short"
    return None
