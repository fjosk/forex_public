#!/usr/bin/env python3
"""octobot_bollinger_band -- OctoBot Bollinger Band Mean Reversion Evaluator. Drakkar-Software."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "octobot_bollinger_band",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, bb_pctb",
    "long": "close < bb_lo (bb_pctb < 0; eval_note = -1 full buy)",
    "short": "close > bb_up (bb_pctb > 1; eval_note = 1 full sell)",
    "desc": "OctoBot BBMomentumEvaluator: full buy/sell at band extremes, parabolic scaling inside",
    "source": "github.com/Drakkar-Software/OctoBot-Tentacles momentum_evaluator/momentum.py",
}


def signal(ind, pos, htf=None):
    """Full signal when bb_pctb < 0 (below lower band) or bb_pctb > 1 (above upper band)."""
    pctb = ind["bb_pctb"][pos]
    if nan(pctb):
        return None
    if pctb < 0:
        return "long"
    if pctb > 1:
        return "short"
    return None
