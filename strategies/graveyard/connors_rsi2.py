#!/usr/bin/env python3
"""connors_rsi2 -- Connors RSI(2) pullback inside the 200-EMA trend.. Ported from sister-lab catalog (https://www.quantifiedstrategies.com/rsi-2-strategy/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "connors_rsi2", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "1h-1d", "indicators": "RSI(2), EMA(200)",
    "long": "close>EMA200 AND RSI2<5", "short": "close<EMA200 AND RSI2>95", "desc": "Connors RSI(2) pullback inside the 200-EMA trend.", "source": "sister-lab catalog: https://www.quantifiedstrategies.com/rsi-2-strategy/",
}


def signal(I, i, htf):
    r2, c, e200 = I["rsi2"][i], I["close"][i], I["ema200"][i]
    if _nan(r2, c, e200):
        return None
    if c > e200 and r2 < 5:          # pullback inside an uptrend
        return "long"
    if c < e200 and r2 > 95:
        return "short"
    return None
