#!/usr/bin/env python3
"""stochastic_cross_oversold -- Stochastic K/D crossover from OB/OS zone. AlgoTest Pine example.

Long when K crosses above D AND K < 20 (oversold zone).
Short when K crosses below D AND K > 80 (overbought zone).
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_cross_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "stoch_k, stoch_d",
    "long": "stoch_k crosses above stoch_d AND stoch_k < 20",
    "short": "stoch_k crosses below stoch_d AND stoch_k > 80",
    "desc": "Stochastic K/D crossover from OB/OS zone; ATR-based TP/SL",
    "source": "web:https://docs.algotest.in/signals/pinescripts/stochastic_oscillator_strategy/",
}


def signal(ind, pos, htf=None):
    """Stochastic K/D crossover from OB/OS zone."""
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(sk, sd, sk1, sd1):
        return None
    if _xup(sk, sk1, sd, sd1) and sk < 20:
        return "long"
    if _xdn(sk, sk1, sd, sd1) and sk > 80:
        return "short"
    return None
