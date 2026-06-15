#!/usr/bin/env python3
"""ao_zero -- Awesome Oscillator zero-line cross.. Ported from sister-lab catalog (https://www.tradingview.com/support/solutions/43000501826-awesome-oscillator-ao/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ao_zero", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-4h", "indicators": "Awesome Oscillator(5,34)",
    "long": "AO crosses above 0", "short": "AO crosses below 0", "desc": "Awesome Oscillator zero-line cross.", "source": "sister-lab catalog: https://www.tradingview.com/support/solutions/43000501826-awesome-oscillator-ao/",
}


def signal(I, i, htf):
    a, a1 = I["ao"][i], I["ao"][i-1]
    if _nan(a, a1):
        return None
    if _xup(a, a1, 0.0, 0.0):
        return "long"
    if _xdn(a, a1, 0.0, 0.0):
        return "short"
    return None
