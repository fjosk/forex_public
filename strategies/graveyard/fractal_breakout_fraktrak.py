#!/usr/bin/env python3
"""fractal_breakout_fraktrak -- Fractal level breakout (Fraktrak Xonax EA). web:mql5.com/14613."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "fractal_breakout_fraktrak",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, frac_up, frac_dn, high, low",
    "long": "high breaks above most recent confirmed upper fractal price (frac_up_px)",
    "short": "low breaks below most recent confirmed lower fractal price (frac_dn_px)",
    "desc": "Fractal breakout: high/low breaks most recent confirmed Williams fractal level (Fraktrak)",
    "source": "web:https://www.mql5.com/en/code/14613",
}


def signal(ind, pos, htf=None):
    """High breaks above frac_up_px, or low breaks below frac_dn_px."""
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    fup_px = ind["frac_up_px"][pos]
    fdn_px = ind["frac_dn_px"][pos]
    fup = ind["frac_up"][pos]
    fdn = ind["frac_dn"][pos]
    if nan(hi, lo, fup_px, fdn_px):
        return None
    # only trade confirmed fractals (frac_up/frac_dn != 0 at some prior bar)
    # frac_up_px holds the price of the last confirmed fractal high
    if hi > fup_px:
        return "long"
    if lo < fdn_px:
        return "short"
    return None
