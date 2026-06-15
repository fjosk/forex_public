#!/usr/bin/env python3
"""directional_movement_system_di_crossover_immediate_entry_case_2 -- Hochheimer DI crossover case 2: market-on-open entry on the bar after the DI cross. Kaufman TSM Ch.23.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "directional_movement_system_di_crossover_immediate_entry_case_2",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "di_plus,di_minus",
    "long": "DI+ crosses above DI- (signal bar); enter next bar at open",
    "short": "DI- crosses above DI+ (signal bar); enter next bar at open",
    "desc": "Hochheimer case 2: immediate DI crossover entry at open of next bar (always in market)",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.23 Hochheimer case 2",
}


def signal(ind, pos, htf=None):
    """DI crossover on prior bar -> enter immediately (modelled as same-bar once crossover confirmed)."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    dip1 = ind["di_plus"][pos - 1]
    dim1 = ind["di_minus"][pos - 1]
    if nan(dip, dim, dip1, dim1):
        return None
    if dip > dim and dip1 <= dim1:
        return "long"
    if dim > dip and dim1 <= dip1:
        return "short"
    return None
