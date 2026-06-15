#!/usr/bin/env python3
"""ema200_rsi_pullback -- EMA200 trend + EMA50 pullback + RSI confirmation. web:https://forexforstarters.com/indicators/combinations/rsi-ema/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema200_rsi_pullback",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema200, ema50, rsi, close, open",
    "long": "close > ema200, price at ema50 zone, rsi >= 40, bullish candle",
    "short": "close < ema200, price at ema50 zone, rsi <= 60, bearish candle",
    "desc": "EMA200 trend with EMA50 pullback and RSI momentum filter",
    "source": "web:https://forexforstarters.com/indicators/combinations/rsi-ema/",
}


def signal(ind, pos, htf=None):
    """Price pulls back to EMA50 in EMA200 trend direction, RSI confirms."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    e200 = ind["ema200"][pos]
    e50 = ind["ema50"][pos]
    rsi = ind["rsi"][pos]
    if nan(c, o, e200, e50, rsi):
        return None
    trend_up = c > e200
    trend_dn = c < e200
    # within 0.2% of ema50
    near_e50 = abs(c - e50) / e50 < 0.002
    bull_candle = c > o
    bear_candle = c < o
    if trend_up and near_e50 and rsi >= 40 and bull_candle:
        return "long"
    if trend_dn and near_e50 and rsi <= 60 and bear_candle:
        return "short"
    return None
