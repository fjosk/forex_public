#!/usr/bin/env python3
"""support_resistance_breakout -- S/R breakout using fractal high/low as mechanical S/R proxy. web:earnforex.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "support_resistance_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, close",
    "long": "close breaks above last fractal high (frac_up_px) -- resistance breakout",
    "short": "close breaks below last fractal low (frac_dn_px) -- support breakdown",
    "desc": "Support/resistance breakout using Williams fractal levels as mechanical S/R proxy",
    "source": "web:https://www.earnforex.com/forex-strategy/support-resistance-strategy/",
}


def signal(ind, pos, htf=None):
    """Fractal S/R breakout on close."""
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    fup, fup1 = ind["frac_up_px"][pos], ind["frac_up_px"][pos - 1]
    fdn, fdn1 = ind["frac_dn_px"][pos], ind["frac_dn_px"][pos - 1]
    if nan(c, c1, fup, fup1, fdn, fdn1):
        return None
    if c > fup and c1 <= fup1:
        return "long"
    if c < fdn and c1 >= fdn1:
        return "short"
    return None
