#!/usr/bin/env python3
"""ut_bot_flip -- UT Bot ATR-trailing-stop flip.. Ported from sister-lab catalog (https://www.tradingview.com/script/n8ss8BID-UT-Bot-Alerts/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ut_bot_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-4h", "indicators": "UT Bot (ATR trailing, k=1, ATR10)",
    "long": "UT position flips long", "short": "UT position flips short", "desc": "UT Bot ATR-trailing-stop flip.", "source": "sister-lab catalog: https://www.tradingview.com/script/n8ss8BID-UT-Bot-Alerts/",
}


def signal(I, i, htf):
    p, p1 = I["ut_pos"][i], I["ut_pos"][i-1]
    if _nan(p, p1):
        return None
    if p == 1 and p1 == -1:
        return "long"
    if p == -1 and p1 == 1:
        return "short"
    return None
