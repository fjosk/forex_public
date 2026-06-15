#!/usr/bin/env python3
"""parabolic_sar_ema50_trend -- PSAR flip aligned with EMA50 trend. forextester.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "parabolic_sar_ema50_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, ema50",
    "long": "close > ema50 AND psar_dir flips from -1 to +1 (SAR flips below price)",
    "short": "close < ema50 AND psar_dir flips from +1 to -1 (SAR flips above price)",
    "desc": "PSAR directional flip with EMA50 trend filter",
    "source": "web:https://forextester.com/blog/parabolic-sar-moving-average-strategy/",
}


def signal(ind, pos, htf=None):
    """PSAR bull/bear flip while on the correct side of EMA50."""
    pd = ind["psar_dir"][pos]
    pdp = ind["psar_dir"][pos - 1]
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(pd, pdp, c, e50):
        return None
    bull_flip = pd == 1 and pdp == -1
    bear_flip = pd == -1 and pdp == 1
    if c > e50 and bull_flip:
        return "long"
    if c < e50 and bear_flip:
        return "short"
    return None
