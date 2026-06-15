#!/usr/bin/env python3
"""stoch_cross_extremes -- Stochastic %K/%D cross inside the oversold/overbought zones.. Ported from sister-lab catalog (https://www.oanda.com/us-en/trade-tap-blog/trading-knowledge/mastering-stochastic-oscillator-trading-strategies/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "stoch_cross_extremes", "cadences": ['day', 'scalp'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-1h", "indicators": "Stochastic(14,3,3)",
    "long": "%K<20 AND %K crosses above %D", "short": "%K>80 AND %K crosses below %D", "desc": "Stochastic %K/%D cross inside the oversold/overbought zones.", "source": "sister-lab catalog: https://www.oanda.com/us-en/trade-tap-blog/trading-knowledge/mastering-stochastic-oscillator-trading-strategies/",
}


def signal(I, i, htf):
    k, d, k1, d1 = I["stoch_k"][i], I["stoch_d"][i], I["stoch_k"][i-1], I["stoch_d"][i-1]
    if _nan(k, d, k1, d1):
        return None
    if k < 20 and _xup(k, k1, d, d1):
        return "long"
    if k > 80 and _xdn(k, k1, d, d1):
        return "short"
    return None
