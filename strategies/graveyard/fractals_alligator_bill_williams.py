#!/usr/bin/env python3
"""fractals_alligator_bill_williams -- Bill Williams fractal above/below Alligator teeth. MQL5 EA."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "fractals_alligator_bill_williams",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "frac_up, frac_dn, frac_up_px, frac_dn_px, al_teeth",
    "long": "confirmed upper fractal AND frac_up_px > al_teeth",
    "short": "confirmed lower fractal AND frac_dn_px < al_teeth",
    "desc": "Bill Williams: fractal breakout above/below Alligator teeth line",
    "source": "web:https://mql5.software/market-news/fractals-alligator-ea-v10-mq4",
}


def signal(ind, pos, htf=None):
    """Upper fractal above teeth = long; lower fractal below teeth = short."""
    fu = ind["frac_up"][pos]
    fd = ind["frac_dn"][pos]
    fu_px = ind["frac_up_px"][pos]
    fd_px = ind["frac_dn_px"][pos]
    teeth = ind["al_teeth"][pos]
    if nan(fu, fd, fu_px, fd_px, teeth):
        return None
    # frac_up != 0 means a confirmed upward fractal exists at this bar
    if fu != 0 and fu_px > teeth:
        return "long"
    if fd != 0 and fd_px < teeth:
        return "short"
    return None
