#!/usr/bin/env python3
"""vr_breakdown_previous_high_low -- Previous day high/low breakout. VOLDEMAR MQL5 EA."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "vr_breakdown_previous_high_low",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "prev_dhh, prev_dll, close",
    "long": "close >= prev_dhh (previous day high touch or break)",
    "short": "close <= prev_dll (previous day low touch or break)",
    "desc": "Previous day high/low breakout: price reaches prior session extreme triggers entry",
    "source": "web:https://www.mql5.com/en/code/69562",
}


def signal(ind, pos, htf=None):
    """Break of the previous day high (long) or low (short)."""
    c = ind["close"][pos]
    pd_hi = ind["prev_dhh"][pos]
    pd_lo = ind["prev_dll"][pos]
    if nan(c, pd_hi, pd_lo):
        return None
    if c >= pd_hi:
        return "long"
    if c <= pd_lo:
        return "short"
    return None
