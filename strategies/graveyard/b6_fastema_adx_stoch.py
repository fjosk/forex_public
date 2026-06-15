#!/usr/bin/env python3
"""b6_fastema_adx_stoch -- BINOPT-06 adapted.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b6_fastema_adx_stoch", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "EMA(5,8,13), ADX, Stochastic",
    "long": "EMA5/8 cross + close>EMA13 + ADX>=20 + stoch", "short": "EMA5/8 cross + close<EMA13 + ADX>=20 + stoch", "desc": "BINOPT-06 adapted.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    e5, e8, e13 = I["ema5"][i], I["ema8"][i], I["ema13"][i]
    e5p, e8p = I["ema5"][i - 1], I["ema8"][i - 1]
    c, adx, k, k1 = I["close"][i], I["adx"][i], I["stoch_k"][i], I["stoch_k"][i - 1]
    if _nan(e5, e8, e13, e5p, e8p, c, adx, k, k1):
        return None
    if e5 > e8 and e5p <= e8p and c > e13 and adx >= 20 and k < 80 and k > k1:
        return "long"
    if e5 < e8 and e5p >= e8p and c < e13 and adx >= 20 and k > 20 and k < k1:
        return "short"
    return None
