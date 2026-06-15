#!/usr/bin/env python3
"""stochastics_overbought_oversold_hook -- Stochastic hook signal: %K crosses %D while both below 30 (rising) or both above 70 (falling). j_person_a_complete_guide_to_technical_trading_tac Ch8."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastics_overbought_oversold_hook",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k,stoch_d",
    "long": "%K crosses above %D AND %K < 30 AND %K is rising (hook up from oversold)",
    "short": "%K crosses below %D AND %K > 70 AND %K is falling (hook down from overbought)",
    "desc": "Stochastic hook: %K/%D crossover with both lines pointing in the direction of the cross inside OB/OS zone",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac, Ch8",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """Long on upward hook in OS; short on downward hook in OB."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(sk, sk1, sd, sd1):
        return None
    # Hook up: %K crosses above %D in OS zone and %K is rising
    if _xup(sk, sk1, sd, sd1) and sk < OS and sk > sk1:
        return "long"
    # Hook down: %K crosses below %D in OB zone and %K is falling
    if _xdn(sk, sk1, sd, sd1) and sk > OB and sk < sk1:
        return "short"
    return None
