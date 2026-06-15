#!/usr/bin/env python3
"""octobot_adx_evaluator -- ADX-gated EMA direction trend signal. OctoBot official Python."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "octobot_adx_evaluator",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx, ema20, close",
    "long": "ADX > 25 AND close < ema20 (price below slow EMA, bullish reversal/pullback)",
    "short": "ADX > 25 AND close > ema20 (price above slow EMA, bearish)",
    "desc": "ADX-gated EMA direction signal: strong trend side determined by close vs EMA20",
    "source": "OctoBot ADXMomentumEvaluator (Drakkar-Software/OctoBot-Tentacles, Python)",
}


def signal(ind, pos, htf=None):
    """ADX > 25 gates the trade; direction is close vs EMA20."""
    adx_val = ind["adx"][pos]
    ema20_val = ind["ema20"][pos]
    c = ind["close"][pos]
    if nan(adx_val, ema20_val, c):
        return None
    if adx_val <= 25:
        return None
    if c < ema20_val:
        return "long"
    if c > ema20_val:
        return "short"
    return None
