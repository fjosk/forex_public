#!/usr/bin/env python3
"""failed_test_prior_high_low_reversal -- Stop-run reversal: marginal break of prior extreme closes back inside. the_new_market_wizards.

Long: bar low pierces Donchian low then closes above it (failed test of low).
Short: bar high pierces Donchian high then closes below it (failed test of high).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "failed_test_prior_high_low_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "dc_up,dc_lo,high,low,close,atr",
    "long": "low < dc_lo (marginal penetration of Donchian low) AND close > dc_lo (closes back above = failed test)",
    "short": "high > dc_up (marginal penetration of Donchian high) AND close < dc_up (closes back below = failed test)",
    "desc": "Failed test stop-run reversal: false break of Donchian extreme with close back inside",
    "source": "the_new_market_wizards, Sperandeo interview pp.105-106",
}


def signal(ind, pos, htf=None):
    """Failed test of prior extreme (Donchian channel) with close reversing back inside."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    atr = ind["atr"][pos]
    if nan(h, l, c, dc_up, dc_lo, atr):
        return None
    # Tolerance: penetration must be modest (< 1 ATR beyond the band)
    tol = atr
    if l < dc_lo and l > dc_lo - tol and c > dc_lo:
        return "long"
    if h > dc_up and h < dc_up + tol and c < dc_up:
        return "short"
    return None
