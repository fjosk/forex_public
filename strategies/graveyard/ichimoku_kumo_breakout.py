#!/usr/bin/env python3
"""ichimoku_kumo_breakout -- Ichimoku Kumo breakout with TK cross confirmation. web:https://trendspider.com/learning-center/ichimoku-cloud-trading-strategies/"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ichimoku_kumo_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "close breaks above cloud AND tenkan crosses above kijun",
    "short": "close breaks below cloud AND tenkan crosses below kijun",
    "desc": "Ichimoku Kumo breakout with TK cross confirmation, TK death cross exit",
    "source": "web:https://trendspider.com/learning-center/ichimoku-cloud-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Kumo breakout confirmed by TK cross -- cleaner than the swing version."""
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
    tk_up = _xup(ten, ten1, kij, kij1)
    tk_dn = _xdn(ten, ten1, kij, kij1)
    if above_cloud and tk_up:
        return "long"
    if below_cloud and tk_dn:
        return "short"
    return None
