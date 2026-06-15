#!/usr/bin/env python3
"""rsi_ema200_extreme_scalp -- RSI2 extreme levels + EMA200 region filter. Zeta-zetra 3-period RSI scalp.

Long when high > ema200 AND rsi2 < 5 (approximates 3-period RSI < 10 extreme).
Short when low < ema200 AND rsi2 > 95 (approximates 3-period RSI > 90 extreme).
rsi2 (2-period) is the closest available substitute for the source's 3-period RSI.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_ema200_extreme_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h",
    "indicators": "ema200, rsi2, high, low",
    "long": "high > ema200 AND rsi2 < 5 (extreme oversold near EMA200)",
    "short": "low < ema200 AND rsi2 > 95 (extreme overbought near EMA200)",
    "desc": "RSI2 extreme mean-reversion with EMA200 region filter; approximates 3-period RSI scalp",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """RSI2 extreme + EMA200 region filter."""
    r2 = ind["rsi2"][pos]
    e200 = ind["ema200"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(r2, e200, h, lo):
        return None
    if h > e200 and r2 < 5:
        return "long"
    if lo < e200 and r2 > 95:
        return "short"
    return None
