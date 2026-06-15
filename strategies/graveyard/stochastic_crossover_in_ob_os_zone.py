#!/usr/bin/env python3
"""stochastic_crossover_in_ob_os_zone -- Stochastic %K/%D crossover while inside OB/OS zone. currency_trading_for_dummies_2nd_edition_by_brian Ch11."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_crossover_in_ob_os_zone",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k,stoch_d",
    "long": "%K crosses up over %D while %K < 20 (oversold crossover)",
    "short": "%K crosses down below %D while %K > 80 (overbought crossover)",
    "desc": "Stochastic %K/%D bullish crossover in OS zone = long; bearish crossover in OB zone = short",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian, Ch11",
}

OB = 80.0
OS = 20.0


def signal(ind, pos, htf=None):
    """Long on %K crossing above %D in oversold; short on %K crossing below %D in overbought."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(sk, sk1, sd, sd1):
        return None
    if _xup(sk, sk1, sd, sd1) and sk < OS:
        return "long"
    if _xdn(sk, sk1, sd, sd1) and sk > OB:
        return "short"
    return None
