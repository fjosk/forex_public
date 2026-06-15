#!/usr/bin/env python3
"""short_term_weekly_reversal -- Per-pair 22-bar ROC reversal; long laggards, short leaders. QuantConnect/Jegadeesh."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "short_term_weekly_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "roc, close",
    "long": "22-bar ROC < -0.02 (pair fell >2% in last month, laggard reversal)",
    "short": "22-bar ROC > +0.02 (pair rose >2% in last month, leader reversal)",
    "desc": "Short-term weekly reversal: fade extreme 22-bar momentum with fixed threshold",
    "source": "QuantConnect Strategy Library (Jegadeesh 1990 reversal); per-pair adaptation",
}

_ROC_LONG_THRESH = -0.02
_ROC_SHORT_THRESH = 0.02


def signal(ind, pos, htf=None):
    """Go long extreme laggards and short extreme leaders over a 22-bar lookback."""
    r = ind["roc"][pos]
    if nan(r):
        return None
    if r < _ROC_LONG_THRESH:
        return "long"
    if r > _ROC_SHORT_THRESH:
        return "short"
    return None
