#!/usr/bin/env python3
"""octobot_golden_death_cross -- EMA50/200 crossover signal on crossover bar only. OctoBot official."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "octobot_golden_death_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema50, ema200",
    "long": "EMA50 crosses above EMA200 (golden cross, on crossover bar only)",
    "short": "EMA50 crosses below EMA200 (death cross, on crossover bar only)",
    "desc": "Golden/death cross: EMA50 vs EMA200 crossover fires only on the crossover bar",
    "source": "OctoBot DeathAndGoldenCrossEvaluator (Drakkar-Software/OctoBot-Tentacles, Python)",
}


def signal(ind, pos, htf=None):
    """Fire only on the bar where EMA50 crosses EMA200."""
    f = ind["ema50"][pos]
    s = ind["ema200"][pos]
    f1 = ind["ema50"][pos - 1]
    s1 = ind["ema200"][pos - 1]
    if nan(f, s, f1, s1):
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
