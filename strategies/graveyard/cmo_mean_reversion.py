#!/usr/bin/env python3
"""cmo_mean_reversion -- Chande Momentum Oscillator mean reversion. Tushar Chande / QuantifiedStrategies.

CMO < -50 (extreme oversold) in a range-bound market (ADX < 25) -> long.
CMO > +50 (extreme overbought) in range mode -> short.
Source: web:https://www.quantifiedstrategies.com/chande-momentum-oscillator-trading-strategy/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cmo_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "cmo, adx",
    "long": "CMO < -50 AND ADX < 25 (range-bound extreme oversold)",
    "short": "CMO > +50 AND ADX < 25 (range-bound extreme overbought)",
    "desc": "CMO mean reversion: fade -50/+50 extremes in ADX-confirmed ranging market",
    "source": "web:https://www.quantifiedstrategies.com/chande-momentum-oscillator-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """CMO fade extremes gated by ADX range-mode filter."""
    cmo = ind["cmo"][pos]
    adx = ind["adx"][pos]
    if nan(cmo, adx):
        return None

    in_range = adx < 25.0

    if in_range and cmo < -50.0:
        return "long"
    if in_range and cmo > 50.0:
        return "short"

    return None
