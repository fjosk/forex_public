#!/usr/bin/env python3
"""chande_kroll_flip -- Chande Kroll stop flip.. Ported from sister-lab catalog (https://www.tradingview.com/support/solutions/43000589105-chande-kroll-stop/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "chande_kroll_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "Chande Kroll Stop(10,1,9)",
    "long": "Close crosses above the short stop", "short": "Close crosses below the long stop", "desc": "Chande Kroll stop flip.", "source": "sister-lab catalog: https://www.tradingview.com/support/solutions/43000589105-chande-kroll-stop/",
}


def signal(I, i, htf):
    c, c1, sl, sl1, ss, ss1 = (I["close"][i], I["close"][i-1], I["ck_long"][i], I["ck_long"][i-1],
                               I["ck_short"][i], I["ck_short"][i-1])
    if _nan(c, c1, sl, sl1, ss, ss1):
        return None
    if c > ss and c1 <= ss1:
        return "long"
    if c < sl and c1 >= sl1:
        return "short"
    return None
