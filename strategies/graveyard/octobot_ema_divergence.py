#!/usr/bin/env python3
"""octobot_ema_divergence -- EMA50 deviation mean-reversion filter. OctoBot official Python."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "octobot_ema_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "ema50, close",
    "long": "close at least 2% below EMA50 (oversold deviation)",
    "short": "close at least 2% above EMA50 (overbought deviation)",
    "desc": "Mean-reversion on EMA50 deviation: enter when price deviates >= 2% from EMA50",
    "source": "OctoBot EMADivergenceTrendEvaluator (Drakkar-Software/OctoBot-Tentacles, Python)",
}


def signal(ind, pos, htf=None):
    """Long when close >= 2% below EMA50; short when close >= 2% above EMA50."""
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    if nan(e50, c) or e50 == 0:
        return None
    pct_diff = (c / e50 - 1.0) * 100.0
    if pct_diff <= -2.0:
        return "long"
    if pct_diff >= 2.0:
        return "short"
    return None
