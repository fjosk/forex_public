#!/usr/bin/env python3
"""triple_ema_8_21_55 -- Triple-EMA ribbon alignment (GMMA-style) trend entry.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/moving-average-trading-strategies).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "triple_ema_8_21_55", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "EMA(8), EMA(21), EMA(50)",
    "long": "EMA8>EMA21>EMA50 and ribbon just turned bullish", "short": "EMA8<EMA21<EMA50 and ribbon just turned bearish", "desc": "Triple-EMA ribbon alignment (GMMA-style) trend entry.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/moving-average-trading-strategies",
}


def signal(I, i, htf):
    e8, e21, e55 = I["ema8"][i], I["ema21"][i], I["ema50"][i]   # 50 stands in for 55
    e8p, e21p = I["ema8"][i-1], I["ema21"][i-1]
    c = I["close"][i]
    if _nan(e8, e21, e55, e8p, e21p, c):
        return None
    if e8 > e21 > e55 and e8p <= e21p:          # ribbon turns fully bullish on this bar
        return "long"
    if e8 < e21 < e55 and e8p >= e21p:
        return "short"
    return None
