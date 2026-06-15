#!/usr/bin/env python3
"""short_long_ma_crossover -- Generic dual MA crossover: fast SMA crosses above/below slow SMA. currency_strategy_a_practitioner_s_guide_to_curren.

Uses SMA20 (fast) / SMA50 (slow) as the representative 20/55-day pair.
Golden cross: SMA20 crosses above SMA50 -> long.
Dead cross: SMA20 crosses below SMA50 -> short.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "short_long_ma_crossover_generic_dual_moving_average",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma20,sma50",
    "long": "SMA20 crosses above SMA50 (golden cross)",
    "short": "SMA20 crosses below SMA50 (dead cross)",
    "desc": "Generic dual MA crossover: SMA20/SMA50 fast/slow crossover for trend entry",
    "source": "currency_strategy_a_practitioner_s_guide_to_curren Ch4 pp93-96",
}


def signal(ind, pos, htf=None):
    """Dual MA crossover: SMA20 vs SMA50."""
    if pos < 1:
        return None
    s20  = ind["sma20"][pos];  s201 = ind["sma20"][pos - 1]
    s50  = ind["sma50"][pos];  s501 = ind["sma50"][pos - 1]
    if nan(s20, s201, s50, s501):
        return None
    if _xup(s20, s201, s50, s501):
        return "long"
    if _xdn(s20, s201, s50, s501):
        return "short"
    return None
