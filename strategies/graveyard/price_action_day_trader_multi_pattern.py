#!/usr/bin/env python3
"""price_action_day_trader_multi_pattern -- Pin bar OR engulfing OR inside-bar breakout, filtered by ema20/ema50 trend.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "price_action_day_trader_multi_pattern",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema20, ema50, open, high, low, close",
    "long": "(pin_bar OR bull_engulf OR inside_bar_breakout_up) AND ema20>ema50",
    "short": "(bear_pin OR bear_engulf OR inside_bar_breakout_dn) AND ema20<ema50",
    "desc": "Multi-pattern PA day trader: pin bar/engulfing/inside-bar gated by EMA20>EMA50 trend",
    "source": "mql5.com/en/code/68704 l2carbon 2026",
}

_BODY_MAX = 0.35
_SHADOW_RATIO = 2.0


def signal(ind, pos, htf=None):
    """Pin bar OR engulfing OR inside-bar breakout, filtered by ema20/ema50."""
    if pos < 2:
        return None
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    op = ind["open"][pos]
    cl = ind["close"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    hi2 = ind["high"][pos - 2]
    lo2 = ind["low"][pos - 2]
    if nan(e20, e50, hi, lo, op, cl, hi1, lo1, o1, c1, hi2, lo2):
        return None

    bull_trend = e20 > e50
    bear_trend = e20 < e50

    # Pin bar detection on current bar
    bar_range = hi - lo
    bull_pin = bear_pin = False
    if bar_range > 0:
        body_size = abs(cl - op)
        body_ratio = body_size / bar_range
        if body_ratio <= _BODY_MAX:
            body_lo = min(op, cl)
            body_hi = max(op, cl)
            lo_shad = max(body_lo - lo, 1e-10)
            hi_shad = max(hi - body_hi, 1e-10)
            bull_pin = lo_shad / hi_shad >= _SHADOW_RATIO
            bear_pin = hi_shad / lo_shad >= _SHADOW_RATIO

    # Engulfing on current vs prior bar
    bull_engulf = (c1 < o1) and (cl > op) and (op < c1) and (cl > o1)
    bear_engulf = (c1 > o1) and (cl < op) and (op > c1) and (cl < o1)

    # Inside bar breakout: bar[-1] inside bar[-2], current bar closes beyond
    is_inside = hi1 < hi2 and lo1 > lo2
    inside_bar_up = is_inside and cl > hi2
    inside_bar_dn = is_inside and cl < lo2

    if bull_trend and (bull_pin or bull_engulf or inside_bar_up):
        return "long"
    if bear_trend and (bear_pin or bear_engulf or inside_bar_dn):
        return "short"
    return None
