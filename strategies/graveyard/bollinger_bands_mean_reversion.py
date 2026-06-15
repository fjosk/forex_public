#!/usr/bin/env python3
"""bollinger_bands_mean_reversion -- Bollinger Bands Mean Reversion. QuantConnect BB Reversal."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_bands_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "bb_lo, bb_up",
    "long": "close < bb_lo (price breaks below lower band)",
    "short": "close > bb_up (price breaks above upper band)",
    "desc": "Enter on BB band touch/break expecting reversion to midline",
    "source": "quantconnect.com/forum/discussion/2865 BB Mean Reversion",
}


def signal(ind, pos, htf=None):
    """Price below lower BB go long; above upper BB go short."""
    c = ind["close"][pos]
    bbl = ind["bb_lo"][pos]
    bbu = ind["bb_up"][pos]
    if nan(c, bbl, bbu):
        return None
    if c < bbl:
        return "long"
    if c > bbu:
        return "short"
    return None
