#!/usr/bin/env python3
"""aroon_crossover -- Aroon-Up/Down crossover with threshold confirmation. QuantifiedStrategies."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "aroon_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h/daily",
    "indicators": "aroon_up, aroon_dn",
    "long": "aroon_up crosses above aroon_dn AND aroon_up > 70 AND aroon_dn < 30",
    "short": "aroon_dn crosses above aroon_up AND aroon_dn > 70 AND aroon_up < 30",
    "desc": "Aroon crossover with strength thresholds for trend momentum entry",
    "source": "web:https://www.quantifiedstrategies.com/aroon-indicator-strategy/",
}


def signal(ind, pos, htf=None):
    """Aroon crossover with threshold filter: up>70 and down<30 for quality."""
    if pos < 1:
        return None
    au0 = ind["aroon_up"][pos]
    ad0 = ind["aroon_dn"][pos]
    au1 = ind["aroon_up"][pos - 1]
    ad1 = ind["aroon_dn"][pos - 1]
    if nan(au0, ad0, au1, ad1):
        return None

    if _xup(au0, au1, ad0, ad1) and au0 > 70 and ad0 < 30:
        return "long"
    if _xdn(au0, au1, ad0, ad1) and ad0 > 70 and au0 < 30:
        return "short"

    return None
