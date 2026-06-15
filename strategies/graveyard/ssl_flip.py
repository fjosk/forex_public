#!/usr/bin/env python3
"""ssl_flip -- SSL channel direction flip.. Ported from sister-lab catalog (https://www.tradingview.com/script/xzIoaIJC-SSL-channel/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ssl_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-4h", "indicators": "SSL channel(10)",
    "long": "SSL flips long", "short": "SSL flips short", "desc": "SSL channel direction flip.", "source": "sister-lab catalog: https://www.tradingview.com/script/xzIoaIJC-SSL-channel/",
}


def signal(I, i, htf):
    h, h1 = I["ssl_hlv"][i], I["ssl_hlv"][i-1]
    if _nan(h, h1):
        return None
    if h == 1 and h1 == -1:
        return "long"
    if h == -1 and h1 == 1:
        return "short"
    return None
