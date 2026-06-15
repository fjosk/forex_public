#!/usr/bin/env python3
"""stochastic_kd_crossover -- Stochastic K/D crossover in OB/OS territory. Zeta-zetra blog.

Long when K crosses above D in oversold zone (K < 20).
Short when K crosses below D in overbought zone (K > 80).
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_kd_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "stoch_k, stoch_d",
    "long": "K crosses above D AND K < 20 (oversold territory crossover)",
    "short": "K crosses below D AND K > 80 (overbought territory crossover)",
    "desc": "Stochastic K/D crossover in OB/OS zone; zeta-zetra implementation",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/blogs/stochastic.html",
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
