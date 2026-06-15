#!/usr/bin/env python3
"""roc_momentum -- Rate-of-change zero-line momentum, trend- and ADX-filtered.. Ported from sister-lab catalog (https://thesecretmindset.com/rate-of-change/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "roc_momentum", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-1d", "indicators": "ROC(9), EMA(50), ADX(14)",
    "long": "ROC crosses above 0 with close>EMA50 and ADX>20", "short": "ROC crosses below 0 with close<EMA50 and ADX>20", "desc": "Rate-of-change zero-line momentum, trend- and ADX-filtered.", "source": "sister-lab catalog: https://thesecretmindset.com/rate-of-change/",
}


def signal(I, i, htf):
    r, r1, c, e50, adx = I["roc"][i], I["roc"][i-1], I["close"][i], I["ema50"][i], I["adx"][i]
    if _nan(r, r1, c, e50, adx):
        return None
    if _xup(r, r1, 0.0, 0.0) and c > e50 and adx > 20:    # ROC turns positive in an uptrend
        return "long"
    if _xdn(r, r1, 0.0, 0.0) and c < e50 and adx > 20:
        return "short"
    return None
