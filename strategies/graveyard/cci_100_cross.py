#!/usr/bin/env python3
"""cci_100_cross -- CCI mean-reversion at the +/-100 thresholds.. Ported from sister-lab catalog (https://www.litefinance.org/blog/for-beginners/best-technical-indicators/commodity-channel-index-cc/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "cci_100_cross", "cadences": ['day'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-4h", "indicators": "CCI(20)",
    "long": "CCI crosses back up through -100", "short": "CCI crosses back down through +100", "desc": "CCI mean-reversion at the +/-100 thresholds.", "source": "sister-lab catalog: https://www.litefinance.org/blog/for-beginners/best-technical-indicators/commodity-channel-index-cc/",
}


def signal(I, i, htf):
    cc, cc1 = I["cci"][i], I["cci"][i-1]
    if _nan(cc, cc1):
        return None
    if _xup(cc, cc1, -100.0, -100.0):       # crosses back up through -100
        return "long"
    if _xdn(cc, cc1, 100.0, 100.0):
        return "short"
    return None
