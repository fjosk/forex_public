#!/usr/bin/env python3
"""range_filter_flip -- DW Range Filter trend flip.. Ported from sister-lab catalog (https://www.tradingview.com/script/lut7sBgG-Range-Filter-DW/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "range_filter_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "5m-1h", "indicators": "Range Filter(14,2.618)",
    "long": "Price above rising range filter (fresh)", "short": "Price below falling range filter (fresh)", "desc": "DW Range Filter trend flip.", "source": "sister-lab catalog: https://www.tradingview.com/script/lut7sBgG-Range-Filter-DW/",
}


def signal(I, i, htf):
    c, c1, f, f1, d = I["close"][i], I["close"][i-1], I["rf_filt"][i], I["rf_filt"][i-1], I["rf_dir"][i]
    if _nan(c, c1, f, f1, d):
        return None
    if c > f and f > f1 and d > 0 and not (c1 > f1):
        return "long"
    if c < f and f < f1 and d < 0 and not (c1 < f1):
        return "short"
    return None
