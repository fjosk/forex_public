#!/usr/bin/env python3
"""supertrend_sma_crossover_ea -- Supertrend + SMA crossover: dual-signal entry with trend confirmation.

No volume -> FX-applicable.
"""
from strategies._common import nan, TREND_FLIP, _xup, _xdn, ALL_CLASSES

META = {
    "id": "supertrend_sma_crossover_ea",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_line, st_dir, sma20, close",
    "long": "close crosses above st_line AND close>sma20; OR close crosses above sma20 while below st_line",
    "short": "close crosses below st_line AND close<sma20; OR close crosses below sma20 while above st_line",
    "desc": "Supertrend + SMA crossover: price crosses Supertrend line with SMA agreement, or SMA cross",
    "source": "tradinformed.com 'Supertrend Trading Strategy EA v2' MQL4",
}


def signal(ind, pos, htf=None):
    """Supertrend + SMA crossover dual-signal entry."""
    if pos < 1:
        return None
    cl0 = ind["close"][pos]
    cl1 = ind["close"][pos - 1]
    st0 = ind["st_line"][pos]
    st1 = ind["st_line"][pos - 1]
    sma0 = ind["sma20"][pos]
    sma1 = ind["sma20"][pos - 1]
    if nan(cl0, cl1, st0, st1, sma0, sma1):
        return None
    # Primary long: close crosses above supertrend AND close > sma20
    st_cross_up = cl0 > st0 and cl1 <= st1
    # Secondary long: close crosses above sma20 while below supertrend
    sma_cross_up = cl0 > sma0 and cl1 <= sma1 and cl0 < st0
    # Primary short: close crosses below supertrend AND close < sma20
    st_cross_dn = cl0 < st0 and cl1 >= st1
    # Secondary short: close crosses below sma20 while above supertrend
    sma_cross_dn = cl0 < sma0 and cl1 >= sma1 and cl0 > st0

    if (st_cross_up and cl0 > sma0) or sma_cross_up:
        return "long"
    if (st_cross_dn and cl0 < sma0) or sma_cross_dn:
        return "short"
    return None
