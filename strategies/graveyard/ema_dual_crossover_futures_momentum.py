#!/usr/bin/env python3
"""ema_dual_crossover_futures_momentum -- EMA Dual Crossover Futures Momentum (QC Lean).
web:https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/FuturesMomentumAlgorithm.py
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_dual_crossover_futures_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "ema20, ema50",
    "long": "ema20 > ema50 * 1.001 (fast > slow by 0.1% tolerance)",
    "short": "ema20 < ema50 * 0.999 (fast < slow by 0.1% tolerance)",
    "desc": "EMA20/50 momentum with 0.1% tolerance band to reduce whipsaws at crossover",
    "source": "web:https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/FuturesMomentumAlgorithm.py",
}

_TOL = 0.001


def signal(ind, pos, htf=None):
    """EMA20 vs EMA50 with tolerance buffer to avoid flat crossover noise."""
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    if nan(e20, e50) or e50 == 0:
        return None
    if e20 > e50 * (1 + _TOL):
        return "long"
    if e20 < e50 * (1 - _TOL):
        return "short"
    return None
