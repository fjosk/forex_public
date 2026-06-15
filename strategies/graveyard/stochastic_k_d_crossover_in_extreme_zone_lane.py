#!/usr/bin/env python3
"""stochastic_k_d_crossover_in_extreme_zone_lane -- Lane stochastic: enter %K/%D crossover only after %D is in an extreme zone (>= 75 or <= 25). trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_k_d_crossover_in_extreme_zone_lane",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k,stoch_d",
    "long": "%D crossed below 25 (extreme low zone) then %K crosses above %D",
    "short": "%D crossed above 75 (extreme high zone) then %K crosses below %D",
    "desc": "Lane stochastic: %K/%D crossover gated by %D having entered the extreme band (75/25)",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

OB = 75.0
OS = 25.0


def signal(ind, pos, htf=None):
    """Long when %K crosses above %D AND %D was in OS band; short on reverse."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(sk, sk1, sd, sd1):
        return None
    # %D must have entered the extreme zone (at least on previous bar or current)
    if _xup(sk, sk1, sd, sd1) and sd1 <= OS:
        return "long"
    if _xdn(sk, sk1, sd, sd1) and sd1 >= OB:
        return "short"
    return None
