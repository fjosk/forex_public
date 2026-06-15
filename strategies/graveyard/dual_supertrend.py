#!/usr/bin/env python3
"""dual_supertrend -- Two-Supertrend agreement (less whipsaw).. Ported from sister-lab catalog (https://www.tradingview.com/scripts/supertrend/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "dual_supertrend", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-1h", "indicators": "Supertrend(10,1)+(10,3)",
    "long": "Both supertrends up and one flipped up", "short": "Both down and one flipped down", "desc": "Two-Supertrend agreement (less whipsaw).", "source": "sister-lab catalog: https://www.tradingview.com/scripts/supertrend/",
}


def signal(I, i, htf):
    sf, ss, sf1, ss1 = I["st_dir_fast"][i], I["st_dir"][i], I["st_dir_fast"][i-1], I["st_dir"][i-1]
    if _nan(sf, ss, sf1, ss1):
        return None
    flipped_up = (sf == 1 and sf1 == -1) or (ss == 1 and ss1 == -1)
    flipped_dn = (sf == -1 and sf1 == 1) or (ss == -1 and ss1 == 1)
    if sf == 1 and ss == 1 and flipped_up:
        return "long"
    if sf == -1 and ss == -1 and flipped_dn:
        return "short"
    return None
