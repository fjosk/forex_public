#!/usr/bin/env python3
"""trix_signal -- Triple-EMA TRIX signal-line cross.. Ported from sister-lab catalog (https://en.wikipedia.org/wiki/Trix_(technical_analysis)).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "trix_signal", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "TRIX(15,9)",
    "long": "TRIX crosses above its signal", "short": "TRIX crosses below its signal", "desc": "Triple-EMA TRIX signal-line cross.", "source": "sister-lab catalog: https://en.wikipedia.org/wiki/Trix_(technical_analysis)",
}


def signal(I, i, htf):
    t, s, t1, s1 = I["trix"][i], I["trix_sig"][i], I["trix"][i-1], I["trix_sig"][i-1]
    if _nan(t, s, t1, s1):
        return None
    if _xup(t, t1, s, s1):
        return "long"
    if _xdn(t, t1, s, s1):
        return "short"
    return None
