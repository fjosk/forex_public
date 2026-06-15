#!/usr/bin/env python3
"""wavetrend_cross -- LazyBear WaveTrend cross in the extreme zones.. Ported from sister-lab catalog (https://github.com/fmzquant/strategies/blob/master/Indicator-WaveTrend-Oscillator.md).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "wavetrend_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-4h", "indicators": "WaveTrend(10,21)",
    "long": "wt1 crosses above wt2 while wt2<=-53 (oversold)", "short": "wt1 crosses below wt2 while wt2>=53", "desc": "LazyBear WaveTrend cross in the extreme zones.", "source": "sister-lab catalog: https://github.com/fmzquant/strategies/blob/master/Indicator-WaveTrend-Oscillator.md",
}


def signal(I, i, htf):
    w1, w2, w11, w21 = I["wt1"][i], I["wt2"][i], I["wt1"][i-1], I["wt2"][i-1]
    if _nan(w1, w2, w11, w21):
        return None
    if _xup(w1, w11, w2, w21) and w2 <= -53:
        return "long"
    if _xdn(w1, w11, w2, w21) and w2 >= 53:
        return "short"
    return None
