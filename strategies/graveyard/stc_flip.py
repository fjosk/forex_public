#!/usr/bin/env python3
"""stc_flip -- Schaff Trend Cycle band flip (faster MACD).. Ported from sister-lab catalog (https://www.quantifiedstrategies.com/schaff-trend-cycle-indicator/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "stc_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-4h", "indicators": "Schaff Trend Cycle(23,50,10)",
    "long": "STC rises through 25", "short": "STC falls through 75", "desc": "Schaff Trend Cycle band flip (faster MACD).", "source": "sister-lab catalog: https://www.quantifiedstrategies.com/schaff-trend-cycle-indicator/",
}


def signal(I, i, htf):
    s, s1 = I["stc"][i], I["stc"][i-1]
    if _nan(s, s1):
        return None
    if s1 < 25 and s >= 25:
        return "long"
    if s1 > 75 and s <= 75:
        return "short"
    return None
