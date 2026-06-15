#!/usr/bin/env python3
"""ema_crossover_heikin_ashi -- EMA Crossover Heikin-Ashi Filter (Strategy001 freqtrade).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Strategy001.py
"""
from strategies._common import nan, _xup, TREND, ALL_CLASSES

META = {
    "id": "ema_crossover_heikin_ashi",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h",
    "indicators": "ema20, ema50, ha_close, ha_open",
    "long": "ema20 crosses above ema50 AND ha_close > ema20 AND ha_open < ha_close (bullish HA)",
    "short": "not implemented",
    "desc": "EMA20/50 crossover with Heikin-Ashi bullish candle confirmation; long-only",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Strategy001.py",
}


def signal(ind, pos, htf=None):
    """Long: EMA20 crosses above EMA50 with HA confirming bullish body above EMA20."""
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    e20_1 = ind["ema20"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    if nan(e20, e50, e20_1, e50_1, hac, hao):
        return None
    if _xup(e20, e20_1, e50, e50_1) and hac > e20 and hao < hac:
        return "long"
    return None
