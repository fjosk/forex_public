#!/usr/bin/env python3
"""b4_macd_200ema -- BINOPT-04 adapted trend pullback.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b4_macd_200ema", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "MACD(12,26,9), EMA(200)",
    "long": "close>EMA200 + MACD cross up near zero", "short": "close<EMA200 + MACD cross down near zero", "desc": "BINOPT-04 adapted trend pullback.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    c, e200 = I["close"][i], I["ema200"][i]
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i - 1], I["macd_sig"][i - 1]
    if _nan(c, e200, m, s, m1, s1):
        return None
    cross_up = m > s and m1 <= s1
    cross_dn = m < s and m1 >= s1
    if c > e200 and cross_up and m <= 0:           # cross up from below/near zero
        return "long"
    if c < e200 and cross_dn and m >= 0:
        return "short"
    return None
