#!/usr/bin/env python3
"""stochastic_rsi_crossover -- StochRSI K/D crossover in extreme zones with EMA200 trend filter. web:quantifiedstrategies.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_rsi_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "srsi_k, srsi_d, ema200",
    "long": "srsi_k crosses above srsi_d while both below 20 and close above ema200",
    "short": "srsi_k crosses below srsi_d while both above 80 and close below ema200",
    "desc": "StochRSI K/D crossover in extreme zones with EMA200 trend filter",
    "source": "web:https://www.quantifiedstrategies.com/stochastic-rsi/",
}


def signal(ind, pos, htf=None):
    """StochRSI crossover in extreme zone, trend-filtered."""
    k, d = ind["srsi_k"][pos], ind["srsi_d"][pos]
    k1, d1 = ind["srsi_k"][pos - 1], ind["srsi_d"][pos - 1]
    c, e200 = ind["close"][pos], ind["ema200"][pos]
    if nan(k, d, k1, d1, c, e200):
        return None
    if _xup(k, k1, d, d1) and d < 20 and c > e200:
        return "long"
    if _xdn(k, k1, d, d1) and d > 80 and c < e200:
        return "short"
    return None
