#!/usr/bin/env python3
"""directional_movement_di_di_crossover_wilder -- Wilder DI+/DI- crossover confirmed by prior-bar high or low penetration. Trade Your Way to Financial Freedom Ch.8.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "directional_movement_di_di_crossover_wilder",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "di_plus,di_minus,high,low",
    "long": "DI+ crosses above DI- AND current high > prior bar high",
    "short": "DI- crosses above DI+ AND current low < prior bar low",
    "desc": "Wilder DI crossover with prior-bar extreme penetration as execution confirmation",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.8 entry signal 1",
}


def signal(ind, pos, htf=None):
    """DI crossover + prior-bar high/low penetration confirmation."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    dip1 = ind["di_plus"][pos - 1]
    dim1 = ind["di_minus"][pos - 1]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(dip, dim, dip1, dim1, hi, lo, hi1, lo1):
        return None
    if dip > dim and dip1 <= dim1 and hi > hi1:
        return "long"
    if dim > dip and dim1 <= dip1 and lo < lo1:
        return "short"
    return None
