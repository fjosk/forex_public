#!/usr/bin/env python3
"""stochastic_ob_os -- Stochastic K exits OB/OS zone with one-bar lookback confirm. barabashkakvn 2018.

Long when stoch_k exits oversold: prior bar < 20 AND current bar > 20.
Short when stoch_k exits overbought: prior bar > 80 AND current bar < 80.
The EA uses a configurable compare_bar; here compare_bar=1 (previous bar).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_ob_os",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "stoch_k",
    "long": "stoch_k[pos-1] < 20 AND stoch_k[pos] > 20 (exits oversold zone)",
    "short": "stoch_k[pos-1] > 80 AND stoch_k[pos] < 80 (exits overbought zone)",
    "desc": "Stochastic exits OB/OS zone: enter on zone-exit crossover; EA barabashkakvn MQL5 2018",
    "source": "web:https://www.mql5.com/en/code/20881",
}


def signal(ind, pos, htf=None):
    """Stochastic K exits OB/OS zone with one-bar confirmation."""
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(sk, sk1):
        return None
    if sk1 < 20 and sk > 20:
        return "long"
    if sk1 > 80 and sk < 80:
        return "short"
    return None
