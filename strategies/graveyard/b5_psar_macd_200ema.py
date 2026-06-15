#!/usr/bin/env python3
"""b5_psar_macd_200ema -- BINOPT-05 adapted triple-confluence trend.. Ported from sister-lab catalog (internal BTCSTRAT/BINOPT dossier).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "b5_psar_macd_200ema", "cadences": ['day'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h", "indicators": "PSAR, MACD hist, EMA(200)",
    "long": "EMA200+PSAR up+hist zero-cross up", "short": "EMA200+PSAR down+hist zero-cross down", "desc": "BINOPT-05 adapted triple-confluence trend.", "source": "sister-lab catalog: internal BTCSTRAT/BINOPT dossier",
}


def signal(I, i, htf):
    c, e200 = I["close"][i], I["ema200"][i]
    pd_, mh, mh1 = I["psar_dir"][i], I["macd_hist"][i], I["macd_hist"][i - 1]
    if _nan(c, e200, mh, mh1):
        return None
    if c > e200 and pd_ > 0 and mh > 0 and mh1 <= 0:   # hist crosses up through zero
        return "long"
    if c < e200 and pd_ < 0 and mh < 0 and mh1 >= 0:
        return "short"
    return None
