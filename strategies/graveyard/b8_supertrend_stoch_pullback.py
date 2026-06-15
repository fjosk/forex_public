#!/usr/bin/env python3
"""b8_supertrend_stoch_pullback -- BINOPT-08 adapted.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b8_supertrend_stoch_pullback", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "Supertrend(10,3), Stochastic",
    "long": "Supertrend up 4 bars + pullback to line + stoch<=20", "short": "Supertrend down 4 bars + pullback + stoch>=80", "desc": "BINOPT-08 adapted.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    d, d1, d2, d3 = (I["st_dir"][i], I["st_dir"][i - 1], I["st_dir"][i - 2], I["st_dir"][i - 3])
    line, lo, hi, k = I["st_line"][i], I["low"][i], I["high"][i], I["stoch_k"][i]
    if _nan(line, lo, hi, k):
        return None
    up = d == 1 and d1 == 1 and d2 == 1 and d3 == 1
    dn = d == -1 and d1 == -1 and d2 == -1 and d3 == -1
    if up and lo <= line * 1.005 and k <= 20:          # pullback touch in uptrend, oversold
        return "long"
    if dn and hi >= line * 0.995 and k >= 80:
        return "short"
    return None
