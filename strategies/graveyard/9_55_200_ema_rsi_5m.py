#!/usr/bin/env python3
"""9_55_200_ema_rsi_5m -- EMA 9/50/200 triple stack with RSI momentum filter 5m scalp. web:fxopen.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "9_55_200_ema_rsi_5m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "5m",
    "indicators": "ema9, ema50, ema200, rsi",
    "long": "EMA9 crosses above EMA50, EMA50 > EMA200 (full bull stack), RSI > 52",
    "short": "EMA9 crosses below EMA50, EMA50 < EMA200 (full bear stack), RSI < 48",
    "desc": "EMA 9/50(55 proxy)/200 triple stack crossover scalp with RSI momentum gate",
    "source": "web:https://fxopen.com/blog/en/three-working-5-minute-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Triple EMA stack crossover (EMA9 x EMA50) with RSI momentum gate."""
    e9, e9_1 = ind["ema9"][pos], ind["ema9"][pos - 1]
    e50, e50_1 = ind["ema50"][pos], ind["ema50"][pos - 1]
    e200 = ind["ema200"][pos]
    rs = ind["rsi"][pos]
    if nan(e9, e9_1, e50, e50_1, e200, rs):
        return None
    if _xup(e9, e9_1, e50, e50_1) and e50 > e200 and rs > 52:
        return "long"
    if _xdn(e9, e9_1, e50, e50_1) and e50 < e200 and rs < 48:
        return "short"
    return None
