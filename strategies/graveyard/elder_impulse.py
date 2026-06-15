#!/usr/bin/env python3
"""elder_impulse -- Elder Impulse System 3-state bar-color transition.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "elder_impulse", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "EMA(13), MACD(12,26,9) hist",
    "long": "Bar turns GREEN (EMA13 up AND MACD-hist up)", "short": "Bar turns RED (EMA13 down AND MACD-hist down)", "desc": "Elder Impulse System 3-state bar-color transition.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system",
}


def signal(I, i, htf):
    """Elder Impulse 3-state bar color: GREEN iff EMA13 rising AND MACD-hist rising; RED iff
    both falling; BLUE otherwise (no-trade). Entry on the transition INTO green/red."""
    e, e1, e2 = I["ema13"][i], I["ema13"][i-1], I["ema13"][i-2]
    h, h1, h2 = I["macd_hist"][i], I["macd_hist"][i-1], I["macd_hist"][i-2]
    if _nan(e, e1, e2, h, h1, h2):
        return None
    green = e > e1 and h > h1
    red = e < e1 and h < h1
    pgreen = e1 > e2 and h1 > h2
    pred = e1 < e2 and h1 < h2
    if green and not pgreen:
        return "long"
    if red and not pred:
        return "short"
    return None
