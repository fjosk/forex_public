#!/usr/bin/env python3
"""donchian_breakout -- Turtle System-1 Donchian breakout (24/7 ORB substitute).. Ported from sister-lab catalog (https://www.altrady.com/blog/crypto-trading-strategies/turtle-trading-strategy-rules).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "donchian_breakout", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "4h-1d", "indicators": "Donchian(20)",
    "long": "Close above the prior 20-bar high", "short": "Close below the prior 20-bar low", "desc": "Turtle System-1 Donchian breakout (24/7 ORB substitute).", "source": "sister-lab catalog: https://www.altrady.com/blog/crypto-trading-strategies/turtle-trading-strategy-rules",
}


def signal(I, i, htf):
    c, up, lo = I["close"][i], I["dc_up"][i], I["dc_lo"][i]
    if _nan(c, up, lo):
        return None
    if c > up:             # close above the prior 20-bar high (Turtle S1)
        return "long"
    if c < lo:
        return "short"
    return None
