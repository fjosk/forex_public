#!/usr/bin/env python3
"""supertrend_rsi_adx_filter -- SuperTrend flip with RSI and ADX filters. beaamoo PineScript."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "supertrend_rsi_adx_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, rsi, adx",
    "long": "st_dir flips bullish AND rsi < 66 AND adx > 20",
    "short": "st_dir flips bearish AND rsi > 34 AND adx > 20",
    "desc": "SuperTrend flip confirmed by RSI within band and ADX trend gate",
    "source": "beaamoo/Supertrend-Strategy-PineScript (modified Leo Smigel TradingView script)",
}


def signal(ind, pos, htf=None):
    """SuperTrend flip gated by RSI level and ADX strength."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    rsi_val = ind["rsi"][pos]
    adx_val = ind["adx"][pos]
    if nan(d, d1, rsi_val, adx_val):
        return None
    flip_bull = d > 0 and d1 <= 0
    flip_bear = d < 0 and d1 >= 0
    if flip_bull and rsi_val < 66 and adx_val > 20:
        return "long"
    if flip_bear and rsi_val > 34 and adx_val > 20:
        return "short"
    return None
