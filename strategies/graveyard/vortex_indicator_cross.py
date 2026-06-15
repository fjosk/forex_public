#!/usr/bin/env python3
"""vortex_indicator_cross -- Vortex Indicator VI+/VI- cross with ADX filter. web:earnforex.com."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "vortex_indicator_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "vi_plus, vi_minus, adx, atr",
    "long": "VI+ crosses above VI- and ADX > 20",
    "short": "VI- crosses above VI+ and ADX > 20",
    "desc": "Vortex Indicator VI+/VI- cross with ADX trend filter",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Vortex VI+/VI- cross filtered by ADX > 20."""
    vp = ind["vi_plus"][pos]
    vm = ind["vi_minus"][pos]
    vp1 = ind["vi_plus"][pos - 1]
    vm1 = ind["vi_minus"][pos - 1]
    adx = ind["adx"][pos]
    if nan(vp, vm, vp1, vm1, adx):
        return None
    if vp > vm and vp1 <= vm1 and adx > 20:
        return "long"
    if vm > vp and vm1 <= vp1 and adx > 20:
        return "short"
    return None
