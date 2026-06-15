#!/usr/bin/env python3
"""stochastic_rsi_macd_crossover -- StochRSI + MACD dual-confirmation entry. web:opofinance.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_rsi_macd_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "srsi_k, srsi_d, macd, macd_sig",
    "long": "srsi_k crosses above srsi_d below 20 AND macd crosses above signal",
    "short": "srsi_k crosses below srsi_d above 80 AND macd crosses below signal",
    "desc": "StochRSI K/D + MACD dual-confirmation reversal entry",
    "source": "web:https://blog.opofinance.com/en/stochastic-rsi-and-macd-strategy/",
}


def signal(ind, pos, htf=None):
    """StochRSI extreme crossover confirmed by MACD crossover."""
    k, d = ind["srsi_k"][pos], ind["srsi_d"][pos]
    k1, d1 = ind["srsi_k"][pos - 1], ind["srsi_d"][pos - 1]
    m, ms = ind["macd"][pos], ind["macd_sig"][pos]
    m1, ms1 = ind["macd"][pos - 1], ind["macd_sig"][pos - 1]
    if nan(k, d, k1, d1, m, ms, m1, ms1):
        return None
    if _xup(k, k1, d, d1) and (k < 20 or d < 20) and _xup(m, m1, ms, ms1):
        return "long"
    if _xdn(k, k1, d, d1) and (k > 80 or d > 80) and _xdn(m, m1, ms, ms1):
        return "short"
    return None
