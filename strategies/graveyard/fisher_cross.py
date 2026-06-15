#!/usr/bin/env python3
"""fisher_cross -- Ehlers Fisher Transform turning point.. Ported from sister-lab catalog (https://www.mesasoftware.com/papers/UsingTheFisherTransform.pdf).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "fisher_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-4h", "indicators": "Fisher Transform(9)",
    "long": "Fisher crosses above trigger while Fisher<0", "short": "Fisher crosses below trigger while Fisher>0", "desc": "Ehlers Fisher Transform turning point.", "source": "sister-lab catalog: https://www.mesasoftware.com/papers/UsingTheFisherTransform.pdf",
}


def signal(I, i, htf):
    f, t, f1, t1 = I["fisher"][i], I["fisher_trig"][i], I["fisher"][i-1], I["fisher_trig"][i-1]
    if _nan(f, t, f1, t1):
        return None
    if _xup(f, f1, t, t1) and f < 0:
        return "long"
    if _xdn(f, f1, t, t1) and f > 0:
        return "short"
    return None
