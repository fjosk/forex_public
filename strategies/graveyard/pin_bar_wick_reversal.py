#!/usr/bin/env python3
"""pin_bar_wick_reversal -- Classic pin bar detection: small body, dominant shadow -> trade opposite.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_wick_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "open, high, low, close",
    "long": "large lower wick dominant (body_ratio<=0.35, lo_shadow/hi_shadow>=2.0)",
    "short": "large upper wick dominant (body_ratio<=0.35, hi_shadow/lo_shadow>=2.0)",
    "desc": "Pin bar wick reversal: small body with dominant shadow signals price rejection",
    "source": "mql5.com/en/code/63971 ExpPinBar artmedia70 2025",
}

_BODY_MAX = 0.35
_SHADOW_RATIO = 2.0


def signal(ind, pos, htf=None):
    """Pin bar wick reversal."""
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    op = ind["open"][pos]
    cl = ind["close"][pos]
    if nan(hi, lo, op, cl):
        return None
    bar_range = hi - lo
    if bar_range <= 0:
        return None
    body_size = abs(cl - op)
    body_ratio = body_size / bar_range
    if body_ratio > _BODY_MAX:
        return None
    body_lo = min(op, cl)
    body_hi = max(op, cl)
    lo_shadow = body_lo - lo
    hi_shadow = hi - body_hi
    # bullish pin bar: lower wick dominant
    if hi_shadow < 1e-10:
        hi_shadow = 1e-10
    if lo_shadow < 1e-10:
        lo_shadow = 1e-10
    if lo_shadow / hi_shadow >= _SHADOW_RATIO:
        return "long"
    # bearish pin bar: upper wick dominant
    if hi_shadow / lo_shadow >= _SHADOW_RATIO:
        return "short"
    return None
