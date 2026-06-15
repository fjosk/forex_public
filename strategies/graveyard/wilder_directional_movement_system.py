#!/usr/bin/env python3
"""wilder_directional_movement_system -- Wilder DRM: +DI/-DI crossover with ADX trend gate. trading_systems_and_methods_kaufman_perry_j_kaufma.

+DI crosses above -DI -> buy (long trend).
-DI crosses above +DI -> sell (short trend).
ADX > 20 required (trend is in motion, not ranging).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "wilder_directional_movement_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus",
    "long": "+DI crosses above -DI with ADX > 20",
    "short": "-DI crosses above +DI with ADX > 20",
    "desc": "Wilder DRM/DMI: +DI/-DI crossover gated by ADX trend strength",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch21 Table21-12 DRM",
}


def signal(ind, pos, htf=None):
    """DI crossover with ADX gate."""
    if pos < 1:
        return None
    dp  = ind["di_plus"][pos];  dp1 = ind["di_plus"][pos - 1]
    dm  = ind["di_minus"][pos]; dm1 = ind["di_minus"][pos - 1]
    dx  = ind["adx"][pos]
    if nan(dp, dp1, dm, dm1, dx):
        return None
    if dx < 20:
        return None
    if _xup(dp, dp1, dm, dm1):
        return "long"
    if _xdn(dp, dp1, dm, dm1):
        return "short"
    return None
