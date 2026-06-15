#!/usr/bin/env python3
"""adx_dmi_di_crossover_with_extreme_point_rule -- DI+/DI- crossover with Wilder extreme-point confirmation and ADX>25 trend gate. Currency Trading for Dummies Ch.11.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_dmi_di_crossover_with_extreme_point_rule",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus,high,low",
    "long": "DI+ crosses above DI- AND ADX>25 AND current high > crossover-bar high (extreme-point rule)",
    "short": "DI- crosses above DI+ AND ADX>25 AND current low < crossover-bar low (extreme-point rule)",
    "desc": "Wilder DI crossover confirmed by the ADX trend gate and the extreme-point (high/low breach) filter",
    "source": "currency_trading_for_dummies_2nd_edition_by_brian Ch.11",
}


def signal(ind, pos, htf=None):
    """DI crossover on the prior bar; confirm with extreme-point price breach this bar."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    dip1 = ind["di_plus"][pos - 1]
    dim1 = ind["di_minus"][pos - 1]
    adx = ind["adx"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(dip, dim, dip1, dim1, adx, hi, lo, hi1, lo1):
        return None
    if adx <= 25:
        return None
    # DI+ crossed above DI- last bar; this bar price must breach that bar's high
    if dip > dim and dip1 <= dim1 and hi > hi1:
        return "long"
    # DI- crossed above DI+ last bar; this bar price must breach that bar's low
    if dim > dip and dim1 <= dip1 and lo < lo1:
        return "short"
    return None
