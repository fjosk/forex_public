#!/usr/bin/env python3
"""stoch_rsi_cross -- Stochastic RSI cross out of the extreme zones.. Ported from sister-lab catalog (https://www.quantifiedstrategies.com/stochastic-rsi/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "stoch_rsi_cross", "cadences": ['day', 'scalp'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-4h", "indicators": "StochRSI(14,14,3,3)",
    "long": "%K<20 AND %K crosses above %D", "short": "%K>80 AND %K crosses below %D", "desc": "Stochastic RSI cross out of the extreme zones.", "source": "sister-lab catalog: https://www.quantifiedstrategies.com/stochastic-rsi/",
}


def signal(I, i, htf):
    k, d, k1, d1 = I["srsi_k"][i], I["srsi_d"][i], I["srsi_k"][i-1], I["srsi_d"][i-1]
    if _nan(k, d, k1, d1):
        return None
    if k < 20 and _xup(k, k1, d, d1):
        return "long"
    if k > 80 and _xdn(k, k1, d, d1):
        return "short"
    return None
