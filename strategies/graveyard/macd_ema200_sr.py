#!/usr/bin/env python3
"""macd_ema200_sr -- MACD bullish cross below zero + close above EMA200. Phantom_Trader_Global."""
from strategies._common import nan, TREND, _xup, _xdn, ALL_CLASSES

META = {
    "id": "macd_ema200_sr",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig, macd_hist, ema200, close",
    "long": "MACD crosses above signal AND MACD < 0 AND close > ema200",
    "short": "MACD crosses below signal AND MACD > 0 AND close < ema200",
    "desc": "MACD zero-cross + EMA200 trend filter with support-resistance context",
    "source": "https://www.tradingview.com/script/FzfWWd0i-MACD-200-EMA-Support-Resistance-Strategy/",
}


def signal(ind, pos, htf=None):
    """MACD cross below/above zero with EMA200 regime filter."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    if nan(m, ms, m1, ms1, e200, c):
        return None
    bull_cross = _xup(m, m1, ms, ms1) and m < 0
    bear_cross = _xdn(m, m1, ms, ms1) and m > 0
    if bull_cross and c > e200:
        return "long"
    if bear_cross and c < e200:
        return "short"
    return None
