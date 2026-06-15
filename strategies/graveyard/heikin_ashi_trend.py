#!/usr/bin/env python3
"""heikin_ashi_trend -- Heikin-Ashi trend continuation with a no-wick strength condition.. Ported from sister-lab catalog (https://www.schwab.com/learn/story/heikin-ashi-candles-reversals-and-strategies).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "heikin_ashi_trend", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "Heikin-Ashi candles, EMA(50)",
    "long": "3 green HA candles, no lower wick, price>EMA50", "short": "3 red HA candles, no upper wick, price<EMA50", "desc": "Heikin-Ashi trend continuation with a no-wick strength condition.", "source": "sister-lab catalog: https://www.schwab.com/learn/story/heikin-ashi-candles-reversals-and-strategies",
}


def signal(I, i, htf):
    # 3 consecutive same-color HA candles with the trend candle's no-wick condition.
    ho, hc = I["ha_open"], I["ha_close"]
    hh, hl = I["high"], I["low"]
    c, e50 = I["close"][i], I["ema50"][i]
    if _nan(ho[i], hc[i], ho[i-1], hc[i-1], ho[i-2], hc[i-2], c, e50):
        return None
    green = hc[i] > ho[i] and hc[i-1] > ho[i-1] and hc[i-2] > ho[i-2]
    red = hc[i] < ho[i] and hc[i-1] < ho[i-1] and hc[i-2] < ho[i-2]
    no_lower = (min(ho[i], hc[i]) - hl[i]) <= 0.1 * (hh[i] - hl[i] + 1e-12)
    no_upper = (hh[i] - max(ho[i], hc[i])) <= 0.1 * (hh[i] - hl[i] + 1e-12)
    if green and no_lower and c > e50:
        return "long"
    if red and no_upper and c < e50:
        return "short"
    return None
