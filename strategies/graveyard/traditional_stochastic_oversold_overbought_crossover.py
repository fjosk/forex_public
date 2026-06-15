#!/usr/bin/env python3
"""traditional_stochastic_oversold_overbought_crossover -- Stochastic 30/70 cross-back-through reversal as described in Naked Forex. naked_forex_high_probability_techniques_for_tradin Ch2."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "traditional_stochastic_oversold_overbought_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k",
    "long": "Stochastic %K was below 30 (oversold) and crosses back above 30",
    "short": "Stochastic %K was above 70 (overbought) and crosses back below 70",
    "desc": "Naked Forex traditional stochastic 70/30 cross-back reversal entry",
    "source": "book: naked_forex_high_probability_techniques_for_tradin, Ch2",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """Long on stoch %K crossing back above 30; short on crossing back below 70."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(sk, sk1):
        return None
    if sk1 < OS and sk >= OS:
        return "long"
    if sk1 > OB and sk <= OB:
        return "short"
    return None
