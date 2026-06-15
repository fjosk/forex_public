#!/usr/bin/env python3
"""dead_cross_ma_crossover_sell -- EMA21 crosses below EMA50 (dead cross); exit long and go short. J. Person Complete Guide to Technical Trading Tactics.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dead_cross_ma_crossover_sell",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema21,ema50",
    "long": "EMA21 crosses above EMA50 (golden cross)",
    "short": "EMA21 crosses below EMA50 (dead cross)",
    "desc": "Dead cross (short MA below long MA) signals bearish trend shift; mirrors golden cross for longs",
    "source": "j_person_a_complete_guide_to_technical_trading_tac Glossary",
}


def signal(ind, pos, htf=None):
    """EMA21/EMA50 crossover: dead cross -> short, golden cross -> long."""
    if pos < 1:
        return None
    f = ind["ema21"][pos]
    f1 = ind["ema21"][pos - 1]
    s = ind["ema50"][pos]
    s1 = ind["ema50"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if f < s and f1 >= s1:
        return "short"
    if f > s and f1 <= s1:
        return "long"
    return None
