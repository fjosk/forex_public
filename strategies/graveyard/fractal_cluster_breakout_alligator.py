#!/usr/bin/env python3
"""fractal_cluster_breakout_alligator -- Fractal breakout above/below last fractal with Alligator filter. web:quantifiedstrategies."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "fractal_cluster_breakout_alligator",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, al_teeth, close",
    "long": "close breaks above last up-fractal price and close is above Alligator teeth",
    "short": "close breaks below last down-fractal price and close is below Alligator teeth",
    "desc": "Fractal breakout above/below last confirmed fractal with Alligator teeth direction filter",
    "source": "web:https://www.quantifiedstrategies.com/fractal-indicator-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Fractal breakout with Alligator filter."""
    c = ind["close"][pos]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    teeth = ind["al_teeth"][pos]
    if nan(c, fup, fdn, teeth):
        return None
    if c > teeth and c > fup:
        return "long"
    if c < teeth and c < fdn:
        return "short"
    return None
