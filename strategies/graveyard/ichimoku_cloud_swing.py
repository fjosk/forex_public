#!/usr/bin/env python3
"""ichimoku_cloud_swing -- Ichimoku swing: price above cloud + TK cross. web:https://www.fxcm.com/uk/insights/ichimoku-swing-trading-system/"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_swing",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "close above cloud AND tenkan crosses above kijun",
    "short": "close below cloud AND tenkan crosses below kijun",
    "desc": "Ichimoku swing: cloud bias with TK cross entry, Kijun trail exit",
    "source": "web:https://www.fxcm.com/uk/insights/ichimoku-swing-trading-system/",
}


def signal(ind, pos, htf=None):
    """TK cross in cloud direction -- swing edition (daily TF bias)."""
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij1 = ind["ich_kij"][pos - 1]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    c = ind["close"][pos]
    if nan(ten, kij, ten1, kij1, ia, ib, c):
        return None
    above_cloud = c > max(ia, ib)
    below_cloud = c < min(ia, ib)
    if above_cloud and _xup(ten, ten1, kij, kij1):
        return "long"
    if below_cloud and _xdn(ten, ten1, kij, kij1):
        return "short"
    return None
