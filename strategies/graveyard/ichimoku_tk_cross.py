#!/usr/bin/env python3
"""ichimoku_tk_cross -- Ichimoku strong TK cross: crossover above/below the cloud. web:https://www.babypips.com/learn/forex/ichimoku-kinko-hyo"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ichimoku_tk_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "tenkan crosses above kijun AND crossover is above the cloud (strong signal)",
    "short": "tenkan crosses below kijun AND crossover is below the cloud (strong signal)",
    "desc": "Ichimoku TK cross -- strong signal only (crossover above/below the cloud)",
    "source": "web:https://www.babypips.com/learn/forex/ichimoku-kinko-hyo",
}


def signal(ind, pos, htf=None):
    """Ichimoku TK cross rated strong only when above/below the cloud."""
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij1 = ind["ich_kij"][pos - 1]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    c = ind["close"][pos]
    if nan(ten, kij, ten1, kij1, ia, ib, c):
        return None
    cloud_hi = max(ia, ib)
    cloud_lo = min(ia, ib)
    above_cloud = c > cloud_hi
    below_cloud = c < cloud_lo
    if _xup(ten, ten1, kij, kij1) and above_cloud:
        return "long"
    if _xdn(ten, ten1, kij, kij1) and below_cloud:
        return "short"
    return None
