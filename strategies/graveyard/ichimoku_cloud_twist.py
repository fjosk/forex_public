#!/usr/bin/env python3
"""ichimoku_cloud_twist -- Ichimoku cloud breakout with future kumo twist lookahead. web:https://www.forexfactory.com/thread/569471-ichimoku-trading-system"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_twist",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "close above cloud, tenkan above kijun, future cloud (pos+26) bullish twist",
    "short": "close below cloud, tenkan below kijun, future cloud bearish twist",
    "desc": "Ichimoku with kumo twist lookahead: future cloud direction as directional bias",
    "source": "web:https://www.forexfactory.com/thread/569471-ichimoku-trading-system",
}


def signal(ind, pos, htf=None):
    """Ichimoku cloud breakout with 26-bar forward cloud twist confirmation."""
    arr_len = len(ind["close"])
    if pos + 26 >= arr_len:
        return None
    ten = ind["ich_ten"][pos]
    kij = ind["ich_kij"][pos]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    c = ind["close"][pos]
    # future cloud 26 bars ahead
    ia_fwd = ind["ich_a"][pos + 26]
    ib_fwd = ind["ich_b"][pos + 26]
    if nan(ten, kij, ia, ib, c, ia_fwd, ib_fwd):
        return None
    above_cloud = c > max(ia, ib)
    below_cloud = c < min(ia, ib)
    ten_above = ten > kij
    ten_below = ten < kij
    cloud_fwd_bull = ia_fwd > ib_fwd
    cloud_fwd_bear = ia_fwd < ib_fwd
    if above_cloud and ten_above and cloud_fwd_bull:
        return "long"
    if below_cloud and ten_below and cloud_fwd_bear:
        return "short"
    return None
