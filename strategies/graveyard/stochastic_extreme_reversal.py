#!/usr/bin/env python3
"""stochastic_extreme_reversal -- Stochastic K/D cross in lower/upper half of indicator. earnforex.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_extreme_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "stoch_k, stoch_d",
    "long": "%K crosses above %D AND both lines below 50 (lower half of indicator)",
    "short": "%K crosses below %D AND both lines above 50 (upper half of indicator)",
    "desc": "Stochastic crossover in the lower (<50) or upper (>50) half as mean-reversion entry",
    "source": "web:https://www.earnforex.com/forex-strategy/stochastic-oscillator-strategy/",
}


def signal(ind, pos, htf=None):
    """Stoch K/D crossover in lower (long) or upper (short) half."""
    sk = ind["stoch_k"][pos]
    skp = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sdp = ind["stoch_d"][pos - 1]
    if nan(sk, skp, sd, sdp):
        return None
    cross_up = _xup(sk, skp, sd, sdp)
    cross_dn = _xdn(sk, skp, sd, sdp)
    both_low = sk < 50 and sd < 50
    both_high = sk > 50 and sd > 50
    if cross_up and both_low:
        return "long"
    if cross_dn and both_high:
        return "short"
    return None
