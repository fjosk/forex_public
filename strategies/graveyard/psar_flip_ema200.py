#!/usr/bin/env python3
"""psar_flip_ema200 -- Parabolic SAR flip filtered by the 200 EMA trend.. Ported from sister-lab catalog (https://www.luxalgo.com/blog/how-to-use-parabolic-sar-in-trading-strategies/).

Self-contained (sister-lab catalog helper inlined). Volume-free, engine.precompute indicators only.
"""
from strategies._common import nan, ALL_CLASSES

META = {
    "id": "psar_flip_ema200", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-4h", "indicators": "Parabolic SAR(0.02,0.2), EMA(200)",
    "long": "PSAR flips below price AND close>EMA200", "short": "PSAR flips above price AND close<EMA200", "desc": "Parabolic SAR flip filtered by the 200 EMA trend.", "source": "sister-lab catalog: https://www.luxalgo.com/blog/how-to-use-parabolic-sar-in-trading-strategies/",
}


def signal(I, i, htf=None):
    pdir, pdir1, c, e200 = I["psar_dir"][i], I["psar_dir"][i-1], I["close"][i], I["ema200"][i]
    if nan(pdir, pdir1, c, e200):
        return None
    if pdir == 1 and pdir1 == -1 and c > e200:
        return "long"
    if pdir == -1 and pdir1 == 1 and c < e200:
        return "short"
    return None
