#!/usr/bin/env python3
"""dual_ma_countertrend_entry_profiting_from_the_worst_results -- Fade the fast MA signal while slow MA sets direction. trading_systems_and_methods_kaufman_perry_j_kaufma.

Kaufman: the 'worst' fast/slow MA crossover pair produces the best countertrend timing.
Slow MA (ema50) defines trend regime. Fast MA (ema9) gives the fade entry: if slow trend is UP
and fast MA turns DOWN (cross below), enter LONG (fade the fast short signal). Mirror for down.
"""
from strategies._common import nan, REVERT, ALL_CLASSES, _xdn, _xup

META = {
    "id": "dual_ma_countertrend_entry_profiting_from_the_worst_results",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "close,ema9,ema50",
    "long": "Slow trend up (close>ema50) AND fast EMA9 crosses DOWN (bearish fast signal) -> fade = long",
    "short": "Slow trend down (close<ema50) AND fast EMA9 crosses UP (bullish fast signal) -> fade = short",
    "desc": "Dual-MA countertrend: fade the fast-MA signal when slow MA disagrees (worst-result MA pair as timing)",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Fade the fast MA cross when slow trend is opposite."""
    if pos < 1:
        return None
    c    = ind["close"]
    e9   = ind["ema9"]
    e50  = ind["ema50"]
    if nan(c[pos], e9[pos], e9[pos-1], e50[pos]):
        return None

    # Slow trend up: close above ema50; fast ema9 crosses DOWN below close -> fade = long
    if c[pos] > e50[pos] and _xdn(e9[pos], e9[pos-1], c[pos], c[pos-1]):
        return "long"

    # Slow trend down: close below ema50; fast ema9 crosses UP above close -> fade = short
    if c[pos] < e50[pos] and _xup(e9[pos], e9[pos-1], c[pos], c[pos-1]):
        return "short"

    return None
