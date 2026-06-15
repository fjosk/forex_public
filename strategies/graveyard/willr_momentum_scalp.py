#!/usr/bin/env python3
"""willr_momentum_scalp -- Williams %R OB/OS exit + EMA50 trend filter scalp.

Long:  price above ema50 AND willr crosses above -80 (exits oversold zone).
Short: price below ema50 AND willr crosses below -20 (exits overbought zone).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "willr_momentum_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m-15m",
    "indicators": "willr, ema50",
    "long": "close > ema50 AND willr crosses above -80 (exits oversold)",
    "short": "close < ema50 AND willr crosses below -20 (exits overbought)",
    "desc": "Williams %R oversold/overbought exit + EMA50 trend momentum scalp",
    "source": "web:https://www.litefinance.org/blog/for-beginners/best-technical-indicators/best-indicators-for-scalping/",
}


def signal(ind, pos, htf=None):
    """Williams %R momentum scalp."""
    wr0 = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    ema50 = ind["ema50"][pos]
    c = ind["close"][pos]
    if nan(wr0, wr1, ema50, c):
        return None
    if c > ema50 and wr0 > -80 and wr1 <= -80:
        return "long"
    if c < ema50 and wr0 < -20 and wr1 >= -20:
        return "short"
    return None
