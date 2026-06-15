#!/usr/bin/env python3
"""adx_rsi_directional_filter -- ADX + RSI Directional Filter (Nikhil-Adithyan).
web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_rsi_directional_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "adx, di_plus, di_minus, rsi",
    "long": "ADX>35 AND di_plus < di_minus AND rsi < 50",
    "short": "ADX>35 AND di_plus > di_minus AND rsi > 50",
    "desc": "ADX > 35 strong-trend gate; DI direction combined with RSI midline for entry side",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """Strong trend (ADX>35) with DI direction and RSI midline confirmation."""
    adx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    rs = ind["rsi"][pos]
    if nan(adx, dip, dim, rs):
        return None
    if adx <= 35:
        return None
    if dip < dim and rs < 50:
        return "long"
    if dip > dim and rs > 50:
        return "short"
    return None
