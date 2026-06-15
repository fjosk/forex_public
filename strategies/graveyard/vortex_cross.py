#!/usr/bin/env python3
"""vortex_cross -- Vortex VI+/VI- cross, ADX-gated.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/vortex-indicator).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "vortex_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "Vortex(14), ADX",
    "long": "VI+ crosses above VI- with ADX>20", "short": "VI- crosses above VI+ with ADX>20", "desc": "Vortex VI+/VI- cross, ADX-gated.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/vortex-indicator",
}


def signal(I, i, htf):
    vp, vm, vp1, vm1, adx = I["vi_plus"][i], I["vi_minus"][i], I["vi_plus"][i-1], I["vi_minus"][i-1], I["adx"][i]
    if _nan(vp, vm, vp1, vm1, adx):
        return None
    if _xup(vp, vp1, vm, vm1) and adx > 20:
        return "long"
    if _xup(vm, vm1, vp, vp1) and adx > 20:
        return "short"
    return None
