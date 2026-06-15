#!/usr/bin/env python3
"""go_with_flow_close_momentum -- Close-to-close momentum baseline (Davey entry #1). Kevin Davey.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "go_with_flow_close_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close",
    "long": "close > close[-1]",
    "short": "close < close[-1]",
    "desc": "Go-with-the-flow: buy when close exceeds prior close, sell when below (baseline momentum)",
    "source": "Kevin Davey 'Entry and Exit Confessions of a Champion Trader' entry #1; zeta-zetra.github.io",
}


def signal(ind, pos, htf=None):
    """Close-to-close momentum: trade in direction of last bar's close change."""
    if pos < 1:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c0, c1):
        return None
    if c0 > c1:
        return "long"
    if c0 < c1:
        return "short"
    return None
