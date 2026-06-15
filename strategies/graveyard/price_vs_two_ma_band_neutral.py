#!/usr/bin/env python3
"""price_vs_two_ma_band_neutral -- Price must cross ABOVE both MAs to go long; crosses below either to exit. trading_systems_and_methods_kaufman_perry_j_kaufma.

Long only when close > SMA20 AND close > SMA50.
Short only when close < SMA20 AND close < SMA50.
Entry on the bar where both conditions are first satisfied (requires prior bar to NOT satisfy both).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "price_vs_two_ma_band_neutral",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,sma20,sma50",
    "long": "close crosses above BOTH SMA20 and SMA50 (both conditions newly true)",
    "short": "close crosses below BOTH SMA20 and SMA50 (both conditions newly true)",
    "desc": "Dual MA band: requires price above both MAs for long, below both for short; neutral zone between",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch5 p118-119",
}


def signal(ind, pos, htf=None):
    """Price must cross above/below both MAs; neutral when between them."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    s20  = ind["sma20"][pos]
    s201 = ind["sma20"][pos - 1]
    s50  = ind["sma50"][pos]
    s501 = ind["sma50"][pos - 1]
    if nan(c, c1, s20, s201, s50, s501):
        return None
    above_both_now  = c  > s20  and c  > s50
    above_both_prev = c1 > s201 and c1 > s501
    below_both_now  = c  < s20  and c  < s50
    below_both_prev = c1 < s201 and c1 < s501
    if above_both_now and not above_both_prev:
        return "long"
    if below_both_now and not below_both_prev:
        return "short"
    return None
