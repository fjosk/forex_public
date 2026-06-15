#!/usr/bin/env python3
"""keltner_breakout -- Keltner channel trend breakout.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/keltner-channels).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "keltner_breakout", "cadences": ['day', 'scalp'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "5m-1h", "indicators": "Keltner(EMA20, ATR10, 2)",
    "long": "Close above upper Keltner band, center rising", "short": "Close below lower Keltner band, center falling", "desc": "Keltner channel trend breakout.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/keltner-channels",
}


def signal(I, i, htf):
    c, c1, up, lo, mid, mid5 = I["close"][i], I["close"][i-1], I["kc_up"][i], I["kc_lo"][i], I["kc_mid"][i], I["kc_mid"][i-5]
    if _nan(c, c1, up, lo, mid, mid5):
        return None
    if c > up and mid > mid5:          # close breaks upper band, center rising
        return "long"
    if c < lo and mid < mid5:
        return "short"
    return None
