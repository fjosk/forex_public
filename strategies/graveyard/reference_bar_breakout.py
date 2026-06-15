#!/usr/bin/env python3
"""reference_bar_breakout -- Close above prior bar high / below prior bar low (1-bar channel).
encyclopedia_of_chart_patterns_2nd_ed.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "reference_bar_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "close, high, low",
    "long": "close crosses above prior bar high (reference-bar upside confirmation)",
    "short": "close crosses below prior bar low (reference-bar downside confirmation)",
    "desc": "Reference-bar breakout confirmation: close beyond prior bar extreme signals continuation",
    "source": "book: encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul",
}


def signal(ind, pos, htf=None):
    """Close above prior-bar high -> long; close below prior-bar low -> short."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    h1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(c, h1, lo1):
        return None
    if c > h1:
        return "long"
    if c < lo1:
        return "short"
    return None
