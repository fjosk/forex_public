#!/usr/bin/env python3
"""directional_parabolic_drp_combined_system -- DI direction filter combined with parabolic SAR; both must agree. Kaufman TSM Ch.21 DRP.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "directional_parabolic_drp_combined_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "di_plus,di_minus,psar_dir,close",
    "long": "DI+ > DI- AND psar_dir == 1 (SAR below price, long side)",
    "short": "DI- > DI+ AND psar_dir == -1 (SAR above price, short side)",
    "desc": "Directional Parabolic (DRP): Directional Movement and Parabolic SAR must both agree before entering",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.21 Table 21-12 DRP",
}


def signal(ind, pos, htf=None):
    """DI direction AND parabolic SAR direction both agree -> enter."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    pdir = ind["psar_dir"][pos]
    c = ind["close"][pos]
    if nan(dip, dim, pdir, c):
        return None
    if dip > dim and pdir > 0:
        return "long"
    if dim > dip and pdir < 0:
        return "short"
    return None
