#!/usr/bin/env python3
"""ema_slope_trend_vs_range -- Elder: follow EMA13 slope in trends, fade donchian extremes in ranges. elder_alexander_trading_for_a_living.

In trend (EMA13 rising): enter long when EMA13 slopes up.
In trend (EMA13 falling): enter short when EMA13 slopes down.
This module captures only the trend-following branch (follow strength/weakness).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_slope_trend_vs_range",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close,ema13,atr",
    "long": "EMA13 newly turns up (positive slope over 5 bars) -> follow strength long",
    "short": "EMA13 newly turns down (negative slope over 5 bars) -> follow weakness short",
    "desc": "Follow EMA13 slope in trending regime: long when EMA rises, short when falls",
    "source": "elder_alexander_trading_for_a_living Sec20 p81-85",
}


def signal(ind, pos, htf=None):
    """EMA13 slope change: fire when trend regime begins."""
    if pos < 6:
        return None
    e   = ind["ema13"][pos]
    e5  = ind["ema13"][pos - 5]
    e6  = ind["ema13"][pos - 6]
    a   = ind["atr"][pos]
    if nan(e, e5, e6, a) or a == 0:
        return None
    slope_now  = (e  - e5) / a
    slope_prev = (e5 - e6) / a
    thr = 0.05
    up_now   = slope_now  >  thr
    dn_now   = slope_now  < -thr
    up_prev  = slope_prev >  thr
    dn_prev  = slope_prev < -thr
    if up_now and not up_prev:
        return "long"
    if dn_now and not dn_prev:
        return "short"
    return None
