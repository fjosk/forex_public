#!/usr/bin/env python3
"""macd_hist_divergence -- MACD-histogram divergence with a cross confirmation trigger.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/macd-histogram).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "macd_hist_divergence", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "1h-1d", "indicators": "MACD(12,26,9) histogram",
    "long": "Price lower but histogram higher (bull div) + MACD cross up", "short": "Price higher but histogram lower (bear div) + MACD cross down", "desc": "MACD-histogram divergence with a cross confirmation trigger.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/macd-histogram",
}


def signal(I, i, htf):
    lb = 12
    if i < lb + 1:
        return None
    c, clb = I["close"][i], I["close"][i-lb]
    mh, mhlb = I["macd_hist"][i], I["macd_hist"][i-lb]
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    if _nan(c, clb, mh, mhlb, m, s, m1, s1):
        return None
    # bullish: price lower but histogram higher (momentum diverges), confirmed by MACD cross up
    if c < clb and mh > mhlb and _xup(m, m1, s, s1):
        return "long"
    if c > clb and mh < mhlb and _xdn(m, m1, s, s1):
        return "short"
    return None
