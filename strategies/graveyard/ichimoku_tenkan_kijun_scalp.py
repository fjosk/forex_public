#!/usr/bin/env python3
"""ichimoku_tenkan_kijun_scalp -- TK cross with close above/below cloud. web:theforexgeek.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_tenkan_kijun_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "15m",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b",
    "long": "close > cloud top AND tenkan crosses above kijun",
    "short": "close < cloud bottom AND tenkan crosses below kijun",
    "desc": "Ichimoku Tenkan/Kijun cross scalp with cloud direction filter",
    "source": "web:https://theforexgeek.com/ichimoku-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """TK cross in cloud direction: close must be fully above/below the cloud."""
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ten_p = ind["ich_ten"][pos - 1]
    kij_p = ind["ich_kij"][pos - 1]
    c = ind["close"][pos]
    a = ind["ich_a"][pos]
    b = ind["ich_b"][pos]
    if nan(ten, kij, ten_p, kij_p, c, a, b):
        return None
    top = max(a, b)
    bot = min(a, b)
    if c > top and _xup(ten, ten_p, kij, kij_p):
        return "long"
    if c < bot and _xdn(ten, ten_p, kij, kij_p):
        return "short"
    return None
