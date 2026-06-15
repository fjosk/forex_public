#!/usr/bin/env python3
"""rsi2_ema200_pullback -- RSI-2 extreme pullback above EMA200. Larry Connors RSI-2 adapted to both sides.

Long when close > ema200 (uptrend) and rsi2 < 10 (extreme oversold pullback).
Short when close < ema200 (downtrend) and rsi2 > 90 (extreme overbought pullback).
Source is long-only; short side added symmetrically for FX two-way market.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_ema200_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "ema200, rsi2, close",
    "long": "close > ema200 AND rsi2 < 10 (extreme pullback in uptrend)",
    "short": "close < ema200 AND rsi2 > 90 (extreme rally in downtrend)",
    "desc": "Larry Connors RSI-2 extreme pullback filtered by EMA200 trend direction",
    "source": "web:https://github.com/handiko/RSI-2-Stock-Trading-Strategy-Pinescript",
}


def signal(ind, pos, htf=None):
    """RSI2 extreme pullback in trend direction defined by EMA200."""
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    r2 = ind["rsi2"][pos]
    if nan(c, e200, r2):
        return None
    if c > e200 and r2 < 10:
        return "long"
    if c < e200 and r2 > 90:
        return "short"
    return None
