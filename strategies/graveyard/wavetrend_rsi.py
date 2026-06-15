#!/usr/bin/env python3
"""wavetrend_rsi -- WaveTrend cross gated by RSI (crypto-native).. Ported from sister-lab catalog (https://medium.com/@samuel.mcculloch/lets-take-a-look-at-wavetrend-with-crosses-lazybear-s-indicator-2ece1737f72f).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "wavetrend_rsi", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-1h", "indicators": "WaveTrend + RSI(14)",
    "long": "WT cross up, wt2<-53, RSI<40", "short": "WT cross down, wt2>53, RSI>60", "desc": "WaveTrend cross gated by RSI (crypto-native).", "source": "sister-lab catalog: https://medium.com/@samuel.mcculloch/lets-take-a-look-at-wavetrend-with-crosses-lazybear-s-indicator-2ece1737f72f",
}


def signal(I, i, htf):
    w1, w2, w11, w21, r = I["wt1"][i], I["wt2"][i], I["wt1"][i-1], I["wt2"][i-1], I["rsi"][i]
    if _nan(w1, w2, w11, w21, r):
        return None
    if _xup(w1, w11, w2, w21) and w2 < -53 and r < 40:
        return "long"
    if _xdn(w1, w11, w2, w21) and w2 > 53 and r > 60:
        return "short"
    return None
