#!/usr/bin/env python3
"""bill_williams_fractal_alligator -- Bill Williams Fractal-Alligator Breakout.
web:https://www.mql5.com/en/code/23452
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bill_williams_fractal_alligator",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "any",
    "indicators": "al_jaw, al_teeth, al_lips, frac_up_px, frac_dn_px, close",
    "long": "close > frac_up_px AND frac_up_px above all three Alligator lines",
    "short": "close < frac_dn_px AND frac_dn_px below all three Alligator lines",
    "desc": "Fractal breakout confirmed only when fractal is entirely outside the Alligator mouth",
    "source": "web:https://www.mql5.com/en/code/23452",
}


def signal(ind, pos, htf=None):
    """Fractal breakout valid only when fractal level clears all three Alligator lines."""
    c = ind["close"][pos]
    jaw = ind["al_jaw"][pos]
    teeth = ind["al_teeth"][pos]
    lips = ind["al_lips"][pos]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    if nan(c, jaw, teeth, lips, fup, fdn):
        return None
    up_valid = fup > jaw and fup > teeth and fup > lips
    dn_valid = fdn < jaw and fdn < teeth and fdn < lips
    if c > fup and up_valid:
        return "long"
    if c < fdn and dn_valid:
        return "short"
    return None
