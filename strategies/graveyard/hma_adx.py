#!/usr/bin/env python3
"""hma_adx -- Hull MA slope + ADX confluence.. Ported from sister-lab catalog (https://www.investopedia.com/terms/a/adx.asp).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "hma_adx", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "Hull MA(21), ADX(14)",
    "long": "HMA slope up with ADX>20 and rising", "short": "HMA slope down with ADX>20 and rising", "desc": "Hull MA slope + ADX confluence.", "source": "sister-lab catalog: https://www.investopedia.com/terms/a/adx.asp",
}


def signal(I, i, htf):
    h, h1, h2, adx, adx1 = I["hma21"][i], I["hma21"][i-1], I["hma21"][i-2], I["adx"][i], I["adx"][i-1]
    if _nan(h, h1, h2, adx, adx1):
        return None
    if h > h1 and h1 <= h2 and adx > 20 and adx > adx1:
        return "long"
    if h < h1 and h1 >= h2 and adx > 20 and adx > adx1:
        return "short"
    return None
