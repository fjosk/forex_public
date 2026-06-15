#!/usr/bin/env python3
"""directional_parabolic_system_dm_parabolic_sar_combination -- Wilder DPS: take SAR trades only when DM confirms direction; exit on SAR stop or ADX reversal. Kaufman TSM Ch.6.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "directional_parabolic_system_dm_parabolic_sar_combination",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus,psar_dir,psar,close",
    "long": "DI+ > DI- (DM long) AND parabolic SAR in long mode (psar_dir > 0) AND ADX rising",
    "short": "DI- > DI+ (DM short) AND parabolic SAR in short mode (psar_dir < 0) AND ADX rising",
    "desc": "Wilder Directional Parabolic System: DM trend gate + SAR entry/exit agreement + ADX rising confirmation",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.6 Directional Parabolic System",
}


def signal(ind, pos, htf=None):
    """DM agrees with SAR direction AND ADX is rising -> enter."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    pdir = ind["psar_dir"][pos]
    c = ind["close"][pos]
    if nan(dip, dim, adx, adx1, pdir, c):
        return None
    adx_rising = adx > adx1
    if dip > dim and pdir > 0 and adx_rising:
        return "long"
    if dim > dip and pdir < 0 and adx_rising:
        return "short"
    return None
