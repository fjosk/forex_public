#!/usr/bin/env python3
"""geraked_3maf_triple_ma_fractals -- Triple MA stack with new Williams fractal entry. geraked/metatrader5."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "geraked_3maf_triple_ma_fractals",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema20, ema50, frac_up, frac_dn",
    "long": "ema5 > ema20 > ema50 (bull stack) AND a new up-fractal just appeared",
    "short": "ema5 < ema20 < ema50 (bear stack) AND a new dn-fractal just appeared",
    "desc": "Triple MA stack with Williams fractal as entry timing trigger (geraked 3MAF)",
    "source": "https://github.com/geraked/metatrader5",
}


def signal(ind, pos, htf=None):
    """Triple MA stack + new Williams fractal entry."""
    e5 = ind["ema5"][pos]
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    fu = ind["frac_up"][pos]
    fu1 = ind["frac_up"][pos - 1]
    fd = ind["frac_dn"][pos]
    fd1 = ind["frac_dn"][pos - 1]
    if nan(e5, e20, e50, fu, fu1, fd, fd1):
        return None
    bull_stack = e5 > e20 > e50
    bear_stack = e5 < e20 < e50
    new_up_frac = fu != fu1
    new_dn_frac = fd != fd1
    if bull_stack and new_up_frac:
        return "long"
    if bear_stack and new_dn_frac:
        return "short"
    return None
