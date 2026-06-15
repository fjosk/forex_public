#!/usr/bin/env python3
"""low_bb_0985 -- Low BB 0.985 Threshold. freqtrade berlinguyinca Low_BB.py."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "low_bb_0985",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "bb_lo",
    "long": "close <= 0.98 * bb_lo (price at least 2% below lower BB)",
    "short": "not implemented",
    "desc": "Minimal single-rule: enter long when close is 2% below the lower Bollinger Band",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/Low_BB.py",
}


def signal(ind, pos, htf=None):
    """Close at or below 98% of the lower Bollinger Band."""
    c = ind["close"][pos]
    bbl = ind["bb_lo"][pos]
    if nan(c, bbl):
        return None
    if c <= 0.98 * bbl:
        return "long"
    return None
