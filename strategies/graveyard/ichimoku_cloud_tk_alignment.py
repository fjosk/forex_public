#!/usr/bin/env python3
"""ichimoku_cloud_tk_alignment -- Full Ichimoku alignment: price above cloud, bullish cloud, TK aligned. web:https://trendsandbreakouts.com/ichimoku-cloud"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_tk_alignment",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "price above cloud AND cloud bullish (ich_a > ich_b) AND tenkan above kijun",
    "short": "price below cloud AND cloud bearish AND tenkan below kijun",
    "desc": "Full Ichimoku three-way alignment: cloud position + cloud color + TK alignment",
    "source": "web:https://trendsandbreakouts.com/ichimoku-cloud",
}


def signal(ind, pos, htf=None):
    """All three Ichimoku conditions aligned: price/cloud/TK."""
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    c = ind["close"][pos]
    if nan(ten, kij, ia, ib, c):
        return None
    cloud_hi = max(ia, ib)
    cloud_lo = min(ia, ib)
    above_cloud = c > cloud_hi
    below_cloud = c < cloud_lo
    cloud_bull = ia > ib
    cloud_bear = ia < ib
    tk_bull = ten > kij
    tk_bear = ten < kij
    if above_cloud and cloud_bull and tk_bull:
        return "long"
    if below_cloud and cloud_bear and tk_bear:
        return "short"
    return None
