#!/usr/bin/env python3
"""pivot_point_reversal_swing_high_low -- Fractal swing pivot reversal: buy on confirmed pivot low (fractal down), sell on confirmed pivot high (fractal up). trading_systems_and_methods_kaufman_perry_j_kaufma Ch9."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "pivot_point_reversal_swing_high_low",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "frac_up,frac_dn",
    "long": "Confirmed fractal swing low (frac_dn == 1): buy on bar of confirmation",
    "short": "Confirmed fractal swing high (frac_up == 1): sell on bar of confirmation",
    "desc": "Fractal pivot point reversal: enter long on confirmed swing low, short on confirmed swing high",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch9",
}


def signal(ind, pos, htf=None):
    """Long on confirmed fractal low; short on confirmed fractal high."""
    fu = ind["frac_up"][pos]
    fd = ind["frac_dn"][pos]
    if nan(fu, fd):
        return None
    if fd == 1:
        return "long"
    if fu == 1:
        return "short"
    return None
