#!/usr/bin/env python3
"""pivot_channel_breakout -- Breakout above/below the most recent fractal pivot high/low.
trading_systems_and_methods_kaufman.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "pivot_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "frac_up_px, frac_dn_px, high, low",
    "long": "high breaks above the most recent fractal pivot high (frac_up_px)",
    "short": "low breaks below the most recent fractal pivot low (frac_dn_px)",
    "desc": "Pivot channel breakout: price takes out last fractal pivot high or low",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Break above last fractal pivot high -> long; break below last pivot low -> short."""
    h = ind["high"][pos]
    lo = ind["low"][pos]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    if nan(h, lo, fup, fdn):
        return None
    if h > fup:
        return "long"
    if lo < fdn:
        return "short"
    return None
