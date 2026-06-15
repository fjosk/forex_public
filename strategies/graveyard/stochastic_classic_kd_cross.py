#!/usr/bin/env python3
"""stochastic_classic_kd_cross -- Stochastic K/D cross in OB/OS zone. QC classic stochastic.

Long when K crosses above D while K < 20 (oversold zone crossover).
Short when K crosses below D while K > 80 (overbought zone crossover).
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_classic_kd_cross",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "stoch_k, stoch_d",
    "long": "stoch_k crosses above stoch_d AND stoch_k < 20",
    "short": "stoch_k crosses below stoch_d AND stoch_k > 80",
    "desc": "Stochastic K/D crossover in OB/OS zone; classic mean-reversion entry",
    "source": "web:https://www.quantconnect.com/forum/discussion/6585/",
}


def signal(ind, pos, htf=None):
    """Stochastic K/D zone-filtered crossover."""
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
