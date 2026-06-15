#!/usr/bin/env python3
"""modified_three_crossover_dual_ma_confirming_ma_slope_filter -- Dual MA crossover (SMA20/SMA50) confirmed by slope of a third faster MA (EMA9). trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "modified_three_crossover_dual_ma_confirming_ma_slope_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma20, sma50, ema9",
    "long": "SMA20 crosses above SMA50 AND EMA9 is rising (confirming MA slope up)",
    "short": "SMA20 crosses below SMA50 AND EMA9 is falling (confirming MA slope down)",
    "desc": "Modified three-crossover: dual MA cross gated by slope of a third confirming MA",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch 21 Table 21-10",
}


def signal(ind, pos, htf=None):
    """Dual MA cross confirmed by faster EMA slope."""
    if pos < 1:
        return None
    fast = ind["sma20"][pos]
    fast1 = ind["sma20"][pos - 1]
    slow = ind["sma50"][pos]
    slow1 = ind["sma50"][pos - 1]
    conf = ind["ema9"][pos]
    conf1 = ind["ema9"][pos - 1]
    if nan(fast, fast1, slow, slow1, conf, conf1):
        return None
    if _xup(fast, fast1, slow, slow1) and conf > conf1:
        return "long"
    if _xdn(fast, fast1, slow, slow1) and conf < conf1:
        return "short"
    return None
