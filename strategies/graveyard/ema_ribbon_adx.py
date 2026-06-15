#!/usr/bin/env python3
"""ema_ribbon_adx -- EMA ribbon stacking plus an ADX>25 strength gate.. Ported from sister-lab catalog (https://quantstrategy.io/blog/guppy-multiple-moving-average-how-to-use-in-trading/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ema_ribbon_adx", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "EMA(8,13,21,50), ADX(14)",
    "long": "Ribbon stacks 8>13>21>50 with ADX>25", "short": "Ribbon stacks 8<13<21<50 with ADX>25", "desc": "EMA ribbon stacking plus an ADX>25 strength gate.", "source": "sister-lab catalog: https://quantstrategy.io/blog/guppy-multiple-moving-average-how-to-use-in-trading/",
}


def signal(I, i, htf):
    e8, e13, e21, e50 = I["ema8"][i], I["ema13"][i], I["ema21"][i], I["ema50"][i]
    e8p, e13p = I["ema8"][i-1], I["ema13"][i-1]
    adx = I["adx"][i]
    if _nan(e8, e13, e21, e50, e8p, e13p, adx):
        return None
    if e8 > e13 > e21 > e50 and not (e8p > e13p) and adx > 25:   # ribbon just stacked bullish
        return "long"
    if e8 < e13 < e21 < e50 and not (e8p < e13p) and adx > 25:
        return "short"
    return None
