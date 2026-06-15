#!/usr/bin/env python3
"""b9_mtf_ema_stoch -- BINOPT-09 adapted.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b9_mtf_ema_stoch", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "EMA(200,9,21), ADX, Stoch, 4h slope",
    "long": "MTF pullback long", "short": "MTF pullback short", "desc": "BINOPT-09 adapted.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    c, e200, e9, e21 = I["close"][i], I["ema200"][i], I["ema9"][i], I["ema21"][i]
    adx, k, k1 = I["adx"][i], I["stoch_k"][i], I["stoch_k"][i - 1]
    slope = htf["slope"][i]
    if _nan(c, e200, e9, e21, adx, k, k1):
        return None
    if c > e200 and e9 > e21 and slope > 0 and adx >= 25 and k1 <= 20 and k > 20:
        return "long"
    if c < e200 and e9 < e21 and slope < 0 and adx >= 25 and k1 >= 80 and k < 80:
        return "short"
    return None
