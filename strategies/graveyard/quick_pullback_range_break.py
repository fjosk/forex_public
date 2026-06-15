#!/usr/bin/env python3
"""quick_pullback_range_break -- Post-consolidation range expansion: close breaks the wider reference bar extreme.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "quick_pullback_range_break",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "high, low, close",
    "long": "bar[-2] wider than bar[-1] AND close > high[-2]",
    "short": "bar[-2] wider than bar[-1] AND close < low[-2]",
    "desc": "Quick pullback range break: wider reference bar followed by narrow bar then close breaks the reference extreme",
    "source": "github.com/zeta-zetra/code quick_pullback.py",
}


def signal(ind, pos, htf=None):
    """Post-consolidation expansion: close breaks the wider reference bar."""
    if pos < 2:
        return None
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c0 = ind["close"][pos]
    if nan(h2, l2, h1, l1, c0):
        return None
    # bar-2 wider range than bar-1
    ref_wider = h2 > h1 and l2 < l1
    if not ref_wider:
        return None
    if c0 > h2:
        return "long"
    if c0 < l2:
        return "short"
    return None
