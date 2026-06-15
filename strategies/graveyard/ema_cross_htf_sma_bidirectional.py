#!/usr/bin/env python3
"""ema_cross_htf_sma_bidirectional -- EMA Cross HTF SMA Bidirectional (FReinforcedStrategy).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/futures/FReinforcedStrategy.py
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ema_cross_htf_sma_bidirectional",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h",
    "indicators": "ema8, ema21, sma50, adx",
    "long": "close > sma50 (trend up) AND ema8 crosses above ema21",
    "short": "close < sma50 (trend down) AND ema8 crosses below ema21",
    "desc": "EMA8/21 crossover bidrectional with SMA50 trend filter; sma50 approximates 60m HTF SMA",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/futures/FReinforcedStrategy.py",
}


def signal(ind, pos, htf=None):
    """EMA8/21 cross gated by close position vs SMA50 as trend filter."""
    e8 = ind["ema8"][pos]
    e21 = ind["ema21"][pos]
    e8_1 = ind["ema8"][pos - 1]
    e21_1 = ind["ema21"][pos - 1]
    c = ind["close"][pos]
    sma = ind["sma50"][pos]
    if nan(e8, e21, e8_1, e21_1, c, sma):
        return None
    if c > sma and _xup(e8, e8_1, e21, e21_1):
        return "long"
    if c < sma and _xdn(e8, e8_1, e21, e21_1):
        return "short"
    return None
