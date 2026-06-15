#!/usr/bin/env python3
"""stochastic_oscillator_earnforex -- Stochastic K crosses back through OB/OS threshold. EarnForex EA.

Long when K crosses UP through the lower threshold (20): exits oversold, recovery signal.
Short when K crosses DOWN through the upper threshold (80): exits overbought, reversal signal.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_oscillator_earnforex",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "stoch_k, stoch_d",
    "long": "stoch_k[pos-1] < 20 AND stoch_k[pos] > 20 (K crosses up through lower threshold)",
    "short": "stoch_k[pos-1] > 80 AND stoch_k[pos] < 80 (K crosses down through upper threshold)",
    "desc": "Stochastic K threshold crossover entry: long on OS recovery, short on OB reversal",
    "source": "web:https://www.earnforex.com/metatrader-expert-advisors/stochastic-oscillator/",
}


def signal(ind, pos, htf=None):
    """Stochastic K crosses the OB/OS threshold (exit zone = entry signal)."""
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(sk, sk1):
        return None
    if sk1 < 20 and sk > 20:
        return "long"
    if sk1 > 80 and sk < 80:
        return "short"
    return None
