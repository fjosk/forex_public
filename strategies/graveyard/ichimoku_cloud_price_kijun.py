#!/usr/bin/env python3
"""ichimoku_cloud_price_kijun -- Price above cloud + TK cross. mql5 design-a-trading-system series."""
from strategies._common import nan, TREND, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_price_kijun",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "close > ich_a AND close > ich_b AND tenkan crosses above kijun",
    "short": "close < ich_a AND close < ich_b AND tenkan crosses below kijun",
    "desc": "Ichimoku cloud position + TK cross (Strategy 4 strongest signal from mql5 series)",
    "source": "https://www.mql5.com/en/articles/11081",
}


def signal(ind, pos, htf=None):
    """Cloud position + TK cross combination."""
    ten = ind["ich_ten"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij = ind["ich_kij"][pos]
    kij1 = ind["ich_kij"][pos - 1]
    a = ind["ich_a"][pos]
    b = ind["ich_b"][pos]
    c = ind["close"][pos]
    if nan(ten, ten1, kij, kij1, a, b, c):
        return None
    above_cloud = c > a and c > b
    below_cloud = c < a and c < b
    if above_cloud and _xup(ten, ten1, kij, kij1):
        return "long"
    if below_cloud and _xdn(ten, ten1, kij, kij1):
        return "short"
    return None
