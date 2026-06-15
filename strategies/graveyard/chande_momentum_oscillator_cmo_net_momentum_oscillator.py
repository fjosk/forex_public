#!/usr/bin/env python3
"""chande_momentum_oscillator_cmo_net_momentum_oscillator -- CMO extreme-and-turn reversal: long at deep negative extreme turning up, short at deep positive turning down. trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "chande_momentum_oscillator_cmo_net_momentum_oscillator",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "cmo",
    "long": "CMO was deeply oversold (<= -50) and now ticks up (CMO > CMO[prev])",
    "short": "CMO was deeply overbought (>= +50) and now ticks down",
    "desc": "Chande Momentum Oscillator extreme-and-turn reversal: oversold turn-up = long, overbought turn-down = short",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

OB = 50.0
OS = -50.0


def signal(ind, pos, htf=None):
    """Long when CMO turns up from OS extreme; short when it turns down from OB extreme."""
    if pos < 1:
        return None
    cm = ind["cmo"][pos]
    cm1 = ind["cmo"][pos - 1]
    if nan(cm, cm1):
        return None
    # Turn up from oversold
    if cm1 <= OS and cm > cm1:
        return "long"
    # Turn down from overbought
    if cm1 >= OB and cm < cm1:
        return "short"
    return None
