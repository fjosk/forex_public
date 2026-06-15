#!/usr/bin/env python3
"""pivot_extension_breakout -- Pivot S2/R2 extension level breakout. Zeta-zetra Python.

Long when low < piv_s2 (price dips below second support).
Short when high > piv_r2 (price breaks above second resistance).
Daily-shifted standard pivot points (piv_r2, piv_s2 available directly).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "pivot_extension_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "break",
    "tf": "4h",
    "indicators": "piv_r2, piv_s2, high, low",
    "long": "low < piv_s2 (price breaches second support)",
    "short": "high > piv_r2 (price breaches second resistance)",
    "desc": "Pivot point S2/R2 extension breakout; classic second-level support/resistance breach",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Pivot S2/R2 level breach."""
    r2 = ind["piv_r2"][pos]
    s2 = ind["piv_s2"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(r2, s2, h, lo):
        return None
    if lo < s2:
        return "long"
    if h > r2:
        return "short"
    return None
