#!/usr/bin/env python3
"""short_term_swing_point_ringed_high_low_structure -- Williams-style fractal swing-point breakout. long_term_secrets_to_short_term_trading.

Buy on penetration of the swing-low bar's high (confirmed upswing); sell on penetration of the
swing-high bar's low (confirmed downswing). Maps directly to precomputed fractals.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "short_term_swing_point_ringed_high_low_structure",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "frac_up,frac_dn,frac_up_px,frac_dn_px,close,high,low",
    "long": "fractal low confirmed (frac_dn=1 at prior bar) and current close breaks above fractal low bar's high",
    "short": "fractal high confirmed (frac_up=1 at prior bar) and current close breaks below fractal high bar's low",
    "desc": "Short-term ringed-high/low fractal breakout: enter on penetration of the swing-bar extreme",
    "source": "long_term_secrets_to_short_term_trading, Ch1 pp.15-22",
}


def signal(ind, pos, htf=None):
    """Fractal swing-point breakout signal."""
    if pos < 3:
        return None
    c = ind["close"][pos]
    frac_up = ind["frac_up"][pos - 1]
    frac_dn = ind["frac_dn"][pos - 1]
    frac_up_px = ind["frac_up_px"][pos - 1]
    frac_dn_px = ind["frac_dn_px"][pos - 1]
    if nan(c, frac_up, frac_dn):
        return None
    # frac_dn=1 at pos-1 means a swing low was confirmed; the swing-bar high is frac_dn_px
    # frac_up=1 at pos-1 means a swing high was confirmed; the swing-bar low is frac_up_px
    if frac_dn == 1 and not nan(frac_dn_px) and c > frac_dn_px:
        return "long"
    if frac_up == 1 and not nan(frac_up_px) and c < frac_up_px:
        return "short"
    return None
