#!/usr/bin/env python3
"""triple_ma_crossover_golden_dead -- Triple MA golden/dead cross: fast MA crosses above/below medium AND medium above slow. j_person_a_complete_guide_to_technical_trading_tac.

Default 3/9/18 -> proxied with SMA10/SMA20/SMA50 (closest available triple).
Golden cross: SMA10 crosses above SMA20 AND SMA20 above SMA50 -> long.
Dead cross: SMA10 crosses below SMA20 AND SMA20 below SMA50 -> short.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "triple_ma_crossover_dead_cross_golden_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma10,sma20,sma50",
    "long": "SMA10 crosses above SMA20 AND SMA20 already above SMA50 (golden cross confirmation)",
    "short": "SMA10 crosses below SMA20 AND SMA20 already below SMA50 (dead cross confirmation)",
    "desc": "Triple MA golden/dead cross: SMA10/20/50 ordered alignment + fast-to-medium cross triggers entry",
    "source": "j_person_a_complete_guide_to_technical_trading_tac Ch8 pp137-142",
}


def signal(ind, pos, htf=None):
    """Triple MA crossover: fast crosses medium, with medium vs slow confirming."""
    if pos < 1:
        return None
    s10  = ind["sma10"][pos];  s101 = ind["sma10"][pos - 1]
    s20  = ind["sma20"][pos];  s201 = ind["sma20"][pos - 1]
    s50  = ind["sma50"][pos];  s501 = ind["sma50"][pos - 1]
    if nan(s10, s101, s20, s201, s50, s501):
        return None
    if _xup(s10, s101, s20, s201) and s20 > s50:
        return "long"
    if _xdn(s10, s101, s20, s201) and s20 < s50:
        return "short"
    return None
