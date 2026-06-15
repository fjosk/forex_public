#!/usr/bin/env python3
"""ichimoku_cloud_breakout -- Ichimoku cloud breakout with TK cross + RSI exit filter. web:https://forextester.com/blog/ichimoku-kinko-hyo-trading-strategy/"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, rsi, close",
    "long": "close above cloud AND tenkan crosses above kijun",
    "short": "close below cloud AND tenkan crosses below kijun",
    "desc": "Ichimoku cloud breakout with TK cross confirmation and RSI filter (ForexTester iteration 2)",
    "source": "web:https://forextester.com/blog/ichimoku-kinko-hyo-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Cloud breakout entry confirmed by TK cross."""
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij1 = ind["ich_kij"][pos - 1]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    c = ind["close"][pos]
    rsi = ind["rsi"][pos]
    if nan(ten, kij, ten1, kij1, ia, ib, c, rsi):
        return None
    cloud_hi = max(ia, ib)
    cloud_lo = min(ia, ib)
    above_cloud = c > cloud_hi
    below_cloud = c < cloud_lo
    tk_cross_up = _xup(ten, ten1, kij, kij1)
    tk_cross_dn = _xdn(ten, ten1, kij, kij1)
    if above_cloud and tk_cross_up and rsi < 70:
        return "long"
    if below_cloud and tk_cross_dn and rsi > 30:
        return "short"
    return None
