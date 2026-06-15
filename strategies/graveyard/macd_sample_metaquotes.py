#!/usr/bin/env python3
"""macd_sample_metaquotes -- MetaQuotes canonical MACD sample: cross below/above zero + EMA trend. MT4."""
from strategies._common import nan, TREND, ALL_CLASSES

# ema26 not a named key; ema20 used as trend filter proxy (close to ema26).

META = {
    "id": "macd_sample_metaquotes",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig, ema20",
    "long": "macd < 0 AND macd > macd_sig AND prev_macd < prev_macd_sig AND ema20 rising",
    "short": "macd > 0 AND macd < macd_sig AND prev_macd > prev_macd_sig AND ema20 falling",
    "desc": "MetaQuotes canonical MACD Sample EA: crossover below/above zero + EMA20 trend confirmation",
    "source": "https://www.mql5.com/en/articles/1510",
}

_THRESHOLD = 1e-6  # minimum abs(macd) to avoid entering on noise (original: MACDOpenLevel * Point)


def signal(ind, pos, htf=None):
    """MetaQuotes MACD sample logic."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    if nan(m, ms, m1, ms1, e20, e20_1):
        return None
    # Long: MACD below zero, crosses above signal, EMA rising
    if m < 0 and m > ms and m1 < ms1 and abs(m) > _THRESHOLD and e20 > e20_1:
        return "long"
    # Short: MACD above zero, crosses below signal, EMA falling
    if m > 0 and m < ms and m1 > ms1 and abs(m) > _THRESHOLD and e20 < e20_1:
        return "short"
    return None
