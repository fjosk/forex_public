#!/usr/bin/env python3
"""aroon_cross_trend -- Aroon Oscillator zero-cross with strength filter. EarnForex.

Aroon Oscillator (aroon_osc = aroon_up - aroon_dn) crosses above zero with aroon_up > 70.
Crosses below zero with aroon_dn > 70. Confirms that recent highs/lows are genuine.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "aroon_cross_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "aroon_osc, aroon_up, aroon_dn",
    "long": "aroon_osc crosses above zero and aroon_up > 70",
    "short": "aroon_osc crosses below zero and aroon_dn > 70",
    "desc": "Aroon Oscillator zero-cross trend entry with strength confirmation",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/; Tushar Chande (1994)",
}

_ZERO = 0.0


def signal(ind, pos, htf=None):
    """Aroon oscillator cross with directional strength filter."""
    ao = ind["aroon_osc"][pos]
    ao1 = ind["aroon_osc"][pos - 1]
    aup = ind["aroon_up"][pos]
    adn = ind["aroon_dn"][pos]
    if nan(ao, ao1, aup, adn):
        return None
    if _xup(ao, ao1, _ZERO, _ZERO) and aup > 70:
        return "long"
    if _xdn(ao, ao1, _ZERO, _ZERO) and adn > 70:
        return "short"
    return None
