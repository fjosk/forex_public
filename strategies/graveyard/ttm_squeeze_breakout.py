#!/usr/bin/env python3
"""ttm_squeeze_breakout -- TTM squeeze: volatility compression then directional release.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ttm-squeeze).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ttm_squeeze_breakout", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "15m-4h", "indicators": "Bollinger(20,2), Keltner(20,2,10), MACD hist",
    "long": "Squeeze (BB inside KC) releases with histogram>0 rising", "short": "Squeeze releases with histogram<0 falling", "desc": "TTM squeeze: volatility compression then directional release.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ttm-squeeze",
}


def signal(I, i, htf):
    bbu, bbl, kcu, kcl = I["bb_up"][i], I["bb_lo"][i], I["kc_up"][i], I["kc_lo"][i]
    bbu1, bbl1, kcu1, kcl1 = I["bb_up"][i-1], I["bb_lo"][i-1], I["kc_up"][i-1], I["kc_lo"][i-1]
    mh, mh1 = I["macd_hist"][i], I["macd_hist"][i-1]
    if _nan(bbu, bbl, kcu, kcl, bbu1, bbl1, kcu1, kcl1, mh, mh1):
        return None
    squeezed_prev = bbu1 < kcu1 and bbl1 > kcl1     # BB inside KC last bar
    fired = not (bbu < kcu and bbl > kcl)           # squeeze released this bar
    if squeezed_prev and fired and mh > 0 and mh > mh1:
        return "long"
    if squeezed_prev and fired and mh < 0 and mh < mh1:
        return "short"
    return None
