#!/usr/bin/env python3
"""ema_fan_pullback_scalp -- EMA9/20/50 fanned + pullback to fast EMA + bullish body. web:geekyforex.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_fan_pullback_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema9 (proxy ema8), ema20 (proxy ema21), ema50, body_mom",
    "long": "ema9 > ema20 > ema50 AND close near ema9/ema20 AND bullish rejection candle",
    "short": "ema9 < ema20 < ema50 AND close near ema9/ema20 AND bearish rejection candle",
    "desc": "EMA fan-out pullback scalp: aligned EMAs, price retraces to fast EMA, rejection entry",
    "source": "web:https://www.geekyforex.com/3-ema-scalping-strategy",
}


def signal(ind, pos, htf=None):
    """All three EMAs fanned; price pulls back to fast EMA zone; bullish/bearish body confirms entry."""
    e9 = ind["ema9"][pos]
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    bm = ind["body_mom"][pos]
    if nan(e9, e20, e50, c, o, h, lo, bm):
        return None
    bar_range = h - lo
    if bar_range <= 0:
        return None
    body = abs(c - o)
    # long fan: ema9 > ema20 > ema50
    if e9 > e20 and e20 > e50:
        near_ema = lo <= e9 * 1.0015 and c > e9
        rejection_bull = bm > 0 and (h - c) < body * 0.5
        if near_ema and rejection_bull:
            return "long"
    # short fan: ema9 < ema20 < ema50
    if e9 < e20 and e20 < e50:
        near_ema = h >= e9 * 0.9985 and c < e9
        rejection_bear = bm < 0 and (c - lo) < body * 0.5
        if near_ema and rejection_bear:
            return "short"
    return None
