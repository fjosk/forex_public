#!/usr/bin/env python3
"""golden_cross_ma_crossover_buy -- Golden Cross short-MA crosses above long-MA (SMA50/200). j_person_a_complete_guide_to_technical_trading_tac."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "golden_cross_ma_crossover_buy",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma50, sma200",
    "long": "SMA50 crosses above SMA200 (Golden Cross)",
    "short": "SMA50 crosses below SMA200 (Death Cross, natural opposite exit)",
    "desc": "Golden Cross MA crossover: short MA crosses above long MA for trend entry",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac Glossary golden cross",
}


def signal(ind, pos, htf=None):
    """Golden Cross buy: SMA50 crosses SMA200."""
    if pos < 1:
        return None
    fast = ind["sma50"][pos]
    fast1 = ind["sma50"][pos - 1]
    slow = ind["sma200"][pos]
    slow1 = ind["sma200"][pos - 1]
    if nan(fast, fast1, slow, slow1):
        return None
    if _xup(fast, fast1, slow, slow1):
        return "long"
    if _xdn(fast, fast1, slow, slow1):
        return "short"
    return None
