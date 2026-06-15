#!/usr/bin/env python3
"""vwma_zscore_mean_reversion -- VWMA Z-Score Mean Reversion.
web:https://github.com/armelf/Financial-Algorithms
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "vwma_zscore_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "vwma20, close, bb_up, bb_lo",
    "long": "close > vwma20 (uptrend) AND z-score crosses below -1.5",
    "short": "close < vwma20 (downtrend) AND z-score crosses above +1.0",
    "desc": "Z-score of price vs VWMA20 pullback entry; std approximated via Bollinger band width",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}

# BB bands use 2-sigma by default so sigma ~ (bb_up - bb_lo) / 4
_LONG_THRESH = -1.5
_SHORT_THRESH = 1.0


def signal(ind, pos, htf=None):
    """Z-score crossover vs VWMA: enter pullbacks within the prevailing VWMA trend."""
    c = ind["close"][pos]
    vm = ind["vwma20"][pos]
    bup = ind["bb_up"][pos]
    blo = ind["bb_lo"][pos]
    # previous bar for crossover detection
    c1 = ind["close"][pos - 1]
    vm1 = ind["vwma20"][pos - 1]
    bup1 = ind["bb_up"][pos - 1]
    blo1 = ind["bb_lo"][pos - 1]
    if nan(c, vm, bup, blo, c1, vm1, bup1, blo1):
        return None
    # sigma approximation: half BB half-width
    sigma = (bup - blo) / 4.0
    sigma1 = (bup1 - blo1) / 4.0
    if sigma <= 0 or sigma1 <= 0:
        return None
    z = (c - vm) / sigma
    z1 = (c1 - vm1) / sigma1
    # uptrend pullback: z crosses below threshold
    if c > vm and z < _LONG_THRESH and z1 >= _LONG_THRESH:
        return "long"
    # downtrend rally: z crosses above threshold
    if c < vm and z > _SHORT_THRESH and z1 <= _SHORT_THRESH:
        return "short"
    return None
