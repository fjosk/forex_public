#!/usr/bin/env python3
"""macd_rsi_combined_ea -- MACD + RSI Combined EA. kb.mycoder.pro/MyCoder MT4.

MACD above zero + RSI > 50 = bullish zone, long. MACD below zero + RSI < 50 = short.
EMA20 as optional trend filter: long only if close > ema20, short only if close < ema20.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_rsi_combined_ea",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, rsi, ema20, close",
    "long": "macd > 0 AND rsi > 50 AND close > ema20",
    "short": "macd < 0 AND rsi < 50 AND close < ema20",
    "desc": "MACD zone + RSI momentum + EMA20 trend filter: classic beginner EA combination",
    "source": "web:https://kb.mycoder.pro/apibridge/macdrsi-strategy-for-mt4/",
}


def signal(ind, pos, htf=None):
    """MACD zero-level + RSI midline + EMA20 directional filter."""
    m = ind["macd"][pos]
    r = ind["rsi"][pos]
    e20 = ind["ema20"][pos]
    c = ind["close"][pos]
    if nan(m, r, e20, c):
        return None
    if m > 0 and r > 50 and c > e20:
        return "long"
    if m < 0 and r < 50 and c < e20:
        return "short"
    return None
