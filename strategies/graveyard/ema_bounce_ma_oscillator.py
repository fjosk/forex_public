#!/usr/bin/env python3
"""ema_bounce_ma_oscillator -- EMA bounce entry: candle opens between ema9/ema50 and closes through ema9, RSI filter.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_bounce_ma_oscillator",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema9, ema50, rsi",
    "long": "ema9>ema50 AND open between ema9/ema50 AND close>ema9 AND rsi<50",
    "short": "ema9<ema50 AND open between ema9/ema50 AND close<ema9 AND rsi>50",
    "desc": "EMA bounce: pullback into fast EMA in trending stack, closed-through with RSI confirmation",
    "source": "github.com/zeta-zetra/code moving_average_oscillators.py",
}


def signal(ind, pos, htf=None):
    """EMA bounce: candle opens between ema9/ema50, closes through ema9, RSI filter."""
    e9 = ind["ema9"][pos]
    e50 = ind["ema50"][pos]
    op = ind["open"][pos]
    cl = ind["close"][pos]
    rs = ind["rsi"][pos]
    if nan(e9, e50, op, cl, rs):
        return None
    # long: bull stack, open between ema50 and ema9, close above ema9, rsi not overbought
    if e9 > e50 and op > e50 and op < e9 and cl > e9 and rs < 50:
        return "long"
    # short: bear stack, open between ema9 and ema50, close below ema9, rsi not oversold
    if e9 < e50 and op < e50 and op > e9 and cl < e9 and rs > 50:
        return "short"
    return None
