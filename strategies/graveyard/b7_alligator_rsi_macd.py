#!/usr/bin/env python3
"""b7_alligator_rsi_macd -- BINOPT-07 adapted.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b7_alligator_rsi_macd", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "Alligator, RSI, MACD hist",
    "long": "Alligator up + RSI 50-cross up + hist>0", "short": "Alligator down + RSI 50-cross down + hist<0", "desc": "BINOPT-07 adapted.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    j, t, lp = I["al_jaw"][i], I["al_teeth"][i], I["al_lips"][i]
    j1, lp1 = I["al_jaw"][i - 1], I["al_lips"][i - 1]
    r, r1, mh = I["rsi"][i], I["rsi"][i - 1], I["macd_hist"][i]
    if _nan(j, t, lp, j1, lp1, r, r1, mh):
        return None
    spread, spread1 = lp - j, lp1 - j1
    if lp > t > j and spread > spread1 and r > 50 and r1 <= 50 and mh > 0:
        return "long"
    if lp < t < j and (-spread) > (-spread1) and r < 50 and r1 >= 50 and mh < 0:
        return "short"
    return None
