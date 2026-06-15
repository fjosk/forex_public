#!/usr/bin/env python3
"""dpo_mean_reversion_zero_cross -- DPO zero-line cross as cycle timing signal. quantifiedstrategies.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "dpo_mean_reversion_zero_cross",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "dpo",
    "long": "DPO crosses above zero (detrended price cycle upswing)",
    "short": "DPO crosses below zero (detrended price cycle downswing)",
    "desc": "DPO zero-line cross: buy upward cycle turns, sell downward cycle turns (mean-reversion timing)",
    "source": "web:https://www.quantifiedstrategies.com/detrended-price-oscillator-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """DPO zero-line crossover."""
    dp = ind["dpo"][pos]
    dpp = ind["dpo"][pos - 1]
    if nan(dp, dpp):
        return None
    if dp > 0 and dpp <= 0:
        return "long"
    if dp < 0 and dpp >= 0:
        return "short"
    return None
