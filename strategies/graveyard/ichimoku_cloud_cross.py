#!/usr/bin/env python3
"""ichimoku_cloud_cross -- Simplest Ichimoku: price above cloud top = long, below = short. ntalegeofrey."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_a, ich_b, close",
    "long": "close > max(ich_a, ich_b) -- price above cloud top",
    "short": "close < max(ich_a, ich_b) -- price below cloud top",
    "desc": "Ichimoku cloud breakout: close above/below Kumo top signals trend direction",
    "source": "https://github.com/ntalegeofrey/Implementing-the-Ichimoku-trading-strategy-with-Python",
}


def signal(ind, pos, htf=None):
    """Price vs Ichimoku cloud top."""
    a = ind["ich_a"][pos]
    b = ind["ich_b"][pos]
    c = ind["close"][pos]
    a1 = ind["ich_a"][pos - 1]
    b1 = ind["ich_b"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(a, b, c, a1, b1, c1):
        return None
    cloud_top = max(a, b)
    cloud_top1 = max(a1, b1)
    if c > cloud_top and c1 <= cloud_top1:
        return "long"
    if c < cloud_top and c1 >= cloud_top1:
        return "short"
    return None
