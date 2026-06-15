#!/usr/bin/env python3
"""sma_crossover_adx_trend_filter -- SMA20/50 crossover gated by ADX > 25. armelf Python."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sma_crossover_adx_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma20, sma50, adx, di_plus, di_minus",
    "long": "sma20 >= sma50 AND adx > 25 AND di_plus > di_minus",
    "short": "sma20 <= sma50 AND adx > 25 AND di_minus > di_plus",
    "desc": "SMA20/50 crossover filtered by ADX trend strength; DI+/- adds directional confirmation",
    "source": "armelf/Financial-Algorithms -- SMA 20/50 + Trend + ADX (Python)",
}


def signal(ind, pos, htf=None):
    """SMA alignment gated by ADX strength and DI directional confirmation."""
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    adx_val = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    if nan(s20, s50, adx_val, dip, dim):
        return None
    if adx_val <= 25:
        return None
    if s20 >= s50 and dip > dim:
        return "long"
    if s20 <= s50 and dim > dip:
        return "short"
    return None
