#!/usr/bin/env python3
"""stochrsi_stochastic_of_rsi -- StochRSI extreme-and-turn reversal: long at lower extreme (srsi_k near 0) turning up, short at upper extreme (near 100) turning down. trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochrsi_stochastic_of_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "srsi_k,srsi_d",
    "long": "StochRSI srsi_k at lower extreme (<= 10) and ticking up",
    "short": "StochRSI srsi_k at upper extreme (>= 90) and ticking down",
    "desc": "Stochastic of RSI: enter at extreme and turn (0 = long, 100 = short)",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

OB = 90.0
OS = 10.0


def signal(ind, pos, htf=None):
    """Long when srsi_k turns up from lower extreme; short when it turns down from upper extreme."""
    if pos < 1:
        return None
    sk = ind["srsi_k"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    if nan(sk, sk1):
        return None
    if sk1 <= OS and sk > sk1:
        return "long"
    if sk1 >= OB and sk < sk1:
        return "short"
    return None
