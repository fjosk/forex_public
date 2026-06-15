#!/usr/bin/env python3
"""dev_from_ma -- Generalized MA-deviation reversion using ATR distance.. Ported from sister-lab catalog (https://alchemymarkets.com/education/strategies/mean-reversion/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "dev_from_ma", "cadences": ['day'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-4h", "indicators": "EMA(20), ATR(14)",
    "long": "close < EMA20 - 2*ATR (stretched below mean)", "short": "close > EMA20 + 2*ATR (stretched above mean)", "desc": "Generalized MA-deviation reversion using ATR distance.", "source": "sister-lab catalog: https://alchemymarkets.com/education/strategies/mean-reversion/",
}


def signal(I, i, htf):
    c, e20, atr = I["close"][i], I["ema20"][i], I["atr"][i]
    if _nan(c, e20, atr) or atr <= 0:
        return None
    if c < e20 - 2.0 * atr:        # stretched far below the mean
        return "long"
    if c > e20 + 2.0 * atr:
        return "short"
    return None
