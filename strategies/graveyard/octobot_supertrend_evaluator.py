#!/usr/bin/env python3
"""octobot_supertrend_evaluator -- OctoBot SuperTrend evaluator: st_dir flip in reversals_only mode. Drakkar-Software.

The OctoBot evaluator fires eval_note = -1 (bullish) or +1 (bearish) on Supertrend transitions
(reversals_only mode). Mapped directly to st_dir crossover: long on +1 flip, short on -1 flip.
Uses the standard Supertrend (period 10, factor 3.0) which matches st_dir in the engine.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "octobot_supertrend_evaluator",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, atr",
    "long": "st_dir flips to +1 (OctoBot eval_note -1: Supertrend turns bullish)",
    "short": "st_dir flips to -1 (OctoBot eval_note +1: Supertrend turns bearish)",
    "desc": "OctoBot SuperTrend evaluator: Supertrend direction transition entry (reversals_only mode)",
    "source": "https://raw.githubusercontent.com/Drakkar-Software/OctoBot-Tentacles/master/Evaluator/TA/trend_evaluator/trend.py",
}


def signal(ind, pos, htf=None):
    """Supertrend direction flip (OctoBot reversals_only mode)."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
