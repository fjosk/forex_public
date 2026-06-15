#!/usr/bin/env python3
"""ema_scalp_5_13 -- Fast EMA-cross scalp with a higher-EMA bias filter.. Ported from sister-lab catalog (https://www.sahi.com/blogs/ema-scalping-strategy-the-9-21-crossover-setup).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ema_scalp_5_13", "cadences": ['scalp'], "exit": {'sl_atr': 1.0, 'tp_atr': 1.5, 'trail': True, 'trail_activate_r': 0.8, 'time_stop_h': 8, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "scalp", "tf": "5m-15m", "indicators": "EMA(5), EMA(13), EMA(50)",
    "long": "EMA5 crosses above EMA13 with close>EMA50", "short": "EMA5 crosses below EMA13 with close<EMA50", "desc": "Fast EMA-cross scalp with a higher-EMA bias filter.", "source": "sister-lab catalog: https://www.sahi.com/blogs/ema-scalping-strategy-the-9-21-crossover-setup",
}


def signal(I, i, htf):
    e5, e13, e5p, e13p, e50 = I["ema5"][i], I["ema13"][i], I["ema5"][i-1], I["ema13"][i-1], I["ema50"][i]
    c = I["close"][i]
    if _nan(e5, e13, e5p, e13p, e50, c):
        return None
    if _xup(e5, e5p, e13, e13p) and c > e50:        # fast cross with higher-tf-ish bias
        return "long"
    if _xdn(e5, e5p, e13, e13p) and c < e50:
        return "short"
    return None
