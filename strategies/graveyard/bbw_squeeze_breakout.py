#!/usr/bin/env python3
"""bbw_squeeze_breakout -- Bollinger band-width squeeze breakout.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/bollinger-band-width).

Self-contained (sister-lab catalog helper inlined). Volume-free, engine.precompute indicators only.
"""
from strategies._common import nan, ALL_CLASSES

META = {
    "id": "bbw_squeeze_breakout", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "15m-4h", "indicators": "BB width percentile",
    "long": "BBW percentile<20 then close>upper band", "short": "BBW percentile<20 then close<lower band", "desc": "Bollinger band-width squeeze breakout.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/bollinger-band-width",
}


def signal(I, i, htf=None):
    bw1, c, up, lo = I["bbw_pct"][i-1], I["close"][i], I["bb_up"][i], I["bb_lo"][i]
    if nan(bw1, c, up, lo):
        return None
    if bw1 < 20 and c > up:
        return "long"
    if bw1 < 20 and c < lo:
        return "short"
    return None
