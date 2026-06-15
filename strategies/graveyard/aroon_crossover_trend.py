#!/usr/bin/env python3
"""aroon_crossover_trend -- Aroon Indicator crossover trend system. Tushar Chande / QuantifiedStrategies.

Aroon-Up crosses above Aroon-Down AND Aroon-Up > 70 (strong bull regime) -> long.
Aroon-Down crosses above Aroon-Up AND Aroon-Down > 70 -> short.
Source: web:https://www.quantifiedstrategies.com/aroon-indicator/
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "aroon_crossover_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "aroon_up, aroon_dn, aroon_osc",
    "long": "aroon_up crosses above aroon_dn AND aroon_up > 70 AND aroon_dn < 30",
    "short": "aroon_dn crosses above aroon_up AND aroon_dn > 70 AND aroon_up < 30",
    "desc": "Aroon crossover with strong-trend confirmation (up>70, dn<30)",
    "source": "web:https://www.quantifiedstrategies.com/aroon-indicator/",
}


def signal(ind, pos, htf=None):
    """Aroon crossover trend entry with strength filter."""
    if pos < 1:
        return None
    au = ind["aroon_up"][pos]
    ad = ind["aroon_dn"][pos]
    au1 = ind["aroon_up"][pos - 1]
    ad1 = ind["aroon_dn"][pos - 1]
    if nan(au, ad, au1, ad1):
        return None

    if _xup(au, au1, ad, ad1) and au > 70 and ad < 30:
        return "long"
    if _xdn(au, au1, ad, ad1) and ad > 70 and au < 30:
        return "short"

    return None
