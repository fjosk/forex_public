#!/usr/bin/env python3
"""octobot_ema_momentum_evaluator -- EMA21 threshold band signal. OctoBot official Python."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "octobot_ema_momentum_evaluator",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "ema21, close",
    "long": "close <= EMA21 * 0.98 (at least 2% below EMA21)",
    "short": "close >= EMA21 * 1.02 (at least 2% above EMA21)",
    "desc": "EMA21 threshold band: buy when price >= 2% below EMA21, sell when >= 2% above",
    "source": "OctoBot EMAMomentumEvaluator (Drakkar-Software/OctoBot-Tentacles, Python)",
}


def signal(ind, pos, htf=None):
    """Long when price drops 2% below EMA21; short when price rises 2% above EMA21."""
    e21 = ind["ema21"][pos]
    c = ind["close"][pos]
    if nan(e21, c) or e21 == 0:
        return None
    if c <= e21 * 0.98:
        return "long"
    if c >= e21 * 1.02:
        return "short"
    return None
