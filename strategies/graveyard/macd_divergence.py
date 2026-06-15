#!/usr/bin/env python3
"""macd_divergence -- MACD classic divergence via fractal swing detection. earnforex.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "macd_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "macd, frac_dn, frac_dn_px, frac_up, frac_up_px, close",
    "long": "Bullish divergence: price lower low AND macd higher low over last 10 bars; confirmed by bullish bar",
    "short": "Bearish divergence: price higher high AND macd lower high over last 10 bars; confirmed by bearish bar",
    "desc": "MACD classic divergence: N-bar swing comparison of price and MACD line",
    "source": "web:https://www.earnforex.com/forex-strategy/macd-divergence-strategy/",
}

_LB = 10


def signal(ind, pos, htf=None):
    """MACD divergence via N-bar window comparison of price lows/highs vs MACD lows/highs."""
    if pos < _LB + 1:
        return None
    c = ind["close"][pos]
    mc = ind["macd"][pos]
    if nan(c, mc):
        return None
    # Check window for valid values
    window_c = ind["close"][pos - _LB:pos]
    window_m = ind["macd"][pos - _LB:pos]
    if any(nan(v) for v in window_c) or any(nan(v) for v in window_m):
        return None

    import numpy as np
    lo_c = float(np.min(window_c))
    lo_m = float(np.min(window_m))
    hi_c = float(np.max(window_c))
    hi_m = float(np.max(window_m))

    # Bullish divergence: price lower low, MACD higher low
    price_ll = c < lo_c
    macd_hl = mc > lo_m
    bull_div = price_ll and macd_hl

    # Bearish divergence: price higher high, MACD lower high
    price_hh = c > hi_c
    macd_lh = mc < hi_m
    bear_div = price_hh and macd_lh

    # Confirmation: bullish/bearish bar
    op = ind["open"][pos]
    if nan(op):
        return None
    bull_bar = c > op
    bear_bar = c < op

    if bull_div and bull_bar:
        return "long"
    if bear_div and bear_bar:
        return "short"
    return None
