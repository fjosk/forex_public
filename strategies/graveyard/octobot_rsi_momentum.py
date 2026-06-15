#!/usr/bin/env python3
"""octobot_rsi_momentum -- OctoBot RSI Momentum Evaluator. Drakkar-Software/OctoBot.

RSI <= 30 = full buy signal (eval -1). RSI >= 70 = full sell signal (eval +1).
Threshold mode (is_trend_change_identifier=False).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "octobot_rsi_momentum",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "rsi",
    "long": "rsi <= 30 (oversold threshold, configurable long_threshold)",
    "short": "rsi >= 70 (overbought threshold, configurable short_threshold)",
    "desc": "OctoBot RSI threshold evaluator: oversold/overbought mean-reversion signals",
    "source": "web:https://raw.githubusercontent.com/Drakkar-Software/OctoBot-Tentacles/master/Evaluator/TA/momentum_evaluator/momentum.py",
}


def signal(ind, pos, htf=None):
    """RSI oversold/overbought threshold evaluator."""
    r = ind["rsi"][pos]
    if nan(r):
        return None
    if r <= 30:
        return "long"
    if r >= 70:
        return "short"
    return None
