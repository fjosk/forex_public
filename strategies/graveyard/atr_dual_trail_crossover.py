#!/usr/bin/env python3
"""atr_dual_trail_crossover -- ATR dual trailing-stop crossover (fast vs slow trail). hasnocool/ceyhun pine.

Two ATR-based trailing stops (fast: period 5, mult 0.5; slow: period 10, mult 3.0). Buy when fast
trail crosses above slow trail; sell when it crosses below. Approximated using close/high and the
single available atr key (warm-up is absorbed into the nan guard).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "atr_dual_trail_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "atr, close, high, low",
    "long": "fast ATR trail (5-bar high minus 0.5*ATR) crosses above slow ATR trail (10-bar high minus 3.0*ATR)",
    "short": "fast ATR trail crosses below slow ATR trail",
    "desc": "ATR dual trailing-stop crossover: fast trail vs slow trail direction flip entry",
    "source": "https://github.com/hasnocool/tradingview-pine-scripts (ATR Trailing Stop by ceyhun)",
}


def _trail(ind, pos, period, mult):
    """Highest high over [pos-period+1 .. pos] minus mult * atr[pos]. Returns NaN-sentinel if not warm."""
    if pos < period:
        return None
    hh = max(ind["high"][pos - period + 1: pos + 1])
    return hh - mult * ind["atr"][pos]


def signal(ind, pos, htf=None):
    """Fast ATR trail crosses above/below slow ATR trail."""
    if pos < 11:
        return None
    a_fast = _trail(ind, pos, 5, 0.5)
    b_slow = _trail(ind, pos, 10, 3.0)
    a_fast1 = _trail(ind, pos - 1, 5, 0.5)
    b_slow1 = _trail(ind, pos - 1, 10, 3.0)
    if nan(a_fast, b_slow, a_fast1, b_slow1):
        return None
    if _xup(a_fast, a_fast1, b_slow, b_slow1):
        return "long"
    if _xdn(a_fast, a_fast1, b_slow, b_slow1):
        return "short"
    return None
