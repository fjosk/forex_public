#!/usr/bin/env python3
"""macd_cross_zero -- MACD signal cross gated by zero-line regime confirmation.. Ported from sister-lab catalog (https://www.stockgro.club/blogs/trading/macd-trading-strategy/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "macd_cross_zero", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-4h", "indicators": "MACD(12,26,9)",
    "long": "MACD line crosses above signal AND MACD>0", "short": "MACD line crosses below signal AND MACD<0", "desc": "MACD signal cross gated by zero-line regime confirmation.", "source": "sister-lab catalog: https://www.stockgro.club/blogs/trading/macd-trading-strategy/",
}


def signal(I, i, htf):
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    if _nan(m, s, m1, s1):
        return None
    if _xup(m, m1, s, s1) and m > 0:            # signal cross with zero-line regime confirm
        return "long"
    if _xdn(m, m1, s, s1) and m < 0:
        return "short"
    return None
