#!/usr/bin/env python3
"""quick_rise_spike_reversal_sell -- Long upward spike bar with close near low signals short next bar. encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul.

When prior bar has unusually large range AND close is in the lower quarter of that range, fade next bar.
Symmetric: large down bar with close near high -> long next bar.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "quick_rise_spike_reversal_sell",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "high,low,close,open,atr",
    "long": "prior bar range > 2*ATR AND close in upper 25% of bar range (quick decline, close near high) -> buy next bar",
    "short": "prior bar range > 2*ATR AND close in lower 25% of bar range (quick rise, close near low) -> sell next bar",
    "desc": "Quick-rise/decline spike reversal: large-range bar closing at its extreme predicts counter-move next bar",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul, Ch17 Fig17.6",
}


def signal(ind, pos, htf=None):
    """Spike reversal: large range bar closing near an extreme triggers counter signal next bar."""
    if pos < 1:
        return None
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    atr = ind["atr"][pos]
    if nan(h1, l1, c1, atr):
        return None
    rng1 = h1 - l1
    if rng1 <= 0 or rng1 < 2.0 * atr:
        return None
    # Close in lower 25% of bar range (long spike up, close near low) -> short next bar
    if c1 <= l1 + 0.25 * rng1:
        return "short"
    # Close in upper 25% of bar range (quick decline spike, close near high) -> long next bar
    if c1 >= h1 - 0.25 * rng1:
        return "long"
    return None
