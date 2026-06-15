#!/usr/bin/env python3
"""vegas_tunnel -- Vegas Tunnel 144/169-EMA breakout with built-in reverse.. Ported from sister-lab catalog (https://ftmo.com/en/blog/vegas-tunnel-trading/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "vegas_tunnel", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "1h-4h", "indicators": "EMA(144), EMA(169) tunnel",
    "long": "Close breaks above the 144/169 EMA tunnel", "short": "Close breaks below the tunnel (stop-and-reverse)", "desc": "Vegas Tunnel 144/169-EMA breakout with built-in reverse.", "source": "sister-lab catalog: https://ftmo.com/en/blog/vegas-tunnel-trading/",
}


def signal(I, i, htf):
    c, c1 = I["close"][i], I["close"][i-1]
    a, b, a1, b1 = I["ema144"][i], I["ema169"][i], I["ema144"][i-1], I["ema169"][i-1]
    if _nan(c, c1, a, b, a1, b1):
        return None
    up, lo = max(a, b), min(a, b)
    up1, lo1 = max(a1, b1), min(a1, b1)
    if c > up and c1 <= up1:            # break above the tunnel
        return "long"
    if c < lo and c1 >= lo1:            # break below; stop-and-reverse via exit_opposite
        return "short"
    return None
