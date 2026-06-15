#!/usr/bin/env python3
"""candle_shadow_trend_sr_strength -- Smoothed upper/lower shadow trend signals support/resistance bias. trading_systems_and_methods_kaufman_perry_j_kaufma.

Rising smoothed lower-shadow series => increasing support -> long.
Rising smoothed upper-shadow series => increasing resistance -> short.
Proxy: lo_shadow_sma (smoothed lower shadow) and up_shadow_sma (smoothed upper shadow).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "candle_shadow_trend_sr_strength",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "lo_shadow_sma,up_shadow_sma",
    "long": "lo_shadow_sma rising (lower shadow series increasing = support strengthening)",
    "short": "up_shadow_sma rising (upper shadow series increasing = resistance strengthening)",
    "desc": "Candle shadow trend: rising smoothed lower shadow = bullish support; rising upper shadow = bearish resistance",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch9 p.234",
}


def signal(ind, pos, htf=None):
    """Smoothed shadow direction signals support/resistance bias."""
    if pos < 1:
        return None
    lo_now = ind["lo_shadow_sma"][pos]
    lo_prev = ind["lo_shadow_sma"][pos - 1]
    up_now = ind["up_shadow_sma"][pos]
    up_prev = ind["up_shadow_sma"][pos - 1]
    if nan(lo_now, lo_prev, up_now, up_prev):
        return None
    lo_rising = lo_now > lo_prev
    up_rising = up_now > up_prev
    lo_falling = lo_now < lo_prev
    up_falling = up_now < up_prev
    # Rising lower shadow = support building -> long; rising upper shadow = resistance building -> short
    if lo_rising and up_falling:
        return "long"
    if up_rising and lo_falling:
        return "short"
    return None
