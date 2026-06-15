#!/usr/bin/env python3
"""directional_movement_system_di_crossover_delayed_entry_case_1 -- Hochheimer DI crossover case 1: enter when price reaches the crossover-bar extreme while DI alignment holds. Kaufman TSM Ch.23.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "directional_movement_system_di_crossover_delayed_entry_case_1",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "di_plus,di_minus,high,low",
    "long": "DI+ > DI- (alignment held) AND current high > prior bar high (stop triggered)",
    "short": "DI- > DI+ (alignment held) AND current low < prior bar low (stop triggered)",
    "desc": "Hochheimer case 1: DI crossover places a stop at the crossover-bar extreme; enters only if price reaches it while alignment holds",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.23 Hochheimer case 1",
}


def signal(ind, pos, htf=None):
    """DI alignment persists; trigger when current bar breaches prior-bar extreme (stop-entry proxy)."""
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
    # DI+ dominant this bar and last bar (alignment held after cross); price penetrates prior high
    if dip > dim and dip1 > dim1 and hi > hi1:
        return "long"
    # DI- dominant this bar and last bar; price penetrates prior low
    if dim > dip and dim1 > dip1 and lo < lo1:
        return "short"
    return None
