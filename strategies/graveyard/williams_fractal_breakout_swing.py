#!/usr/bin/env python3
"""williams_fractal_breakout_swing -- Williams fractal breakout swing: close beyond confirmed fractal level. web:medium.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "williams_fractal_breakout_swing",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, close",
    "long": "close breaks above confirmed fractal high (frac_up_px)",
    "short": "close breaks below confirmed fractal low (frac_dn_px)",
    "desc": "Williams fractal breakout swing: close above/below last confirmed fractal level",
    "source": "web:https://medium.com/algorithmic-and-quantitative-trading/the-williams-fractals-swing-trading-strategy-pinpointing-support-resistance-for-high-probability-c0ced6c2e7c2",
}


def signal(ind, pos, htf=None):
    """Fractal breakout: close crosses above/below the last confirmed fractal price."""
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
