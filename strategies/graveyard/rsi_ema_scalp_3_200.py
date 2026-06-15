#!/usr/bin/env python3
"""rsi_ema_scalp_3_200 -- RSI(2) extreme oversold/overbought above/below EMA200. zeta-zetra.

Source uses RSI(3); approximated with rsi2 (closest available short-period RSI).
Thresholds adjusted: rsi2<10 -> long; rsi2>90 -> short; with ema200 trend filter.
No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_ema_scalp_3_200",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "ema200, rsi2, high, low",
    "long": "high > ema200 AND rsi2 < 10 (extremely oversold above trend)",
    "short": "high < ema200 AND rsi2 > 90 (extremely overbought below trend)",
    "desc": "RSI(2) extreme scalp: extreme rsi2 oversold/overbought filtered by EMA200 trend direction",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/youtube/rsi_ema_scalping.html",
}


def signal(ind, pos, htf=None):
    """Extreme RSI(2) scalp with EMA200 trend filter."""
    e200 = ind["ema200"][pos]
    rs2 = ind["rsi2"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(e200, rs2, hi, lo):
        return None
    if hi > e200 and rs2 < 10:
        return "long"
    if lo < e200 and rs2 > 90:
        return "short"
    return None
