#!/usr/bin/env python3
"""smash_day_reversal_naked_close_type -- Naked-close day closes beyond prior extreme; next bar
penetrates smash-day range to confirm reversal. long_term_secrets_to_short_term_trading.

Smash-day buy: close[pos-1] < low[pos-2] (naked down close), then high[pos] > high[pos-1].
Smash-day sell: close[pos-1] > high[pos-2] (naked up close), then low[pos] < low[pos-1].
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "smash_day_reversal_naked_close_type",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "close,high,low",
    "long": "prior bar closes below the bar-before low (naked down close); current bar trades above prior bar high",
    "short": "prior bar closes above the bar-before high (naked up close); current bar trades below prior bar low",
    "desc": "Smash Day Reversal: naked-close setup then next-bar penetration of smash-day extreme confirms reversal",
    "source": "long_term_secrets_to_short_term_trading Ch.7 Figures 7.7-7.9",
}


def signal(ind, pos, htf=None):
    """Smash day: naked close beyond prior extreme, confirmed by next bar."""
    if pos < 2:
        return None
    c1  = ind["close"][pos - 1]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    lo2 = ind["low"][pos - 2]
    hi2 = ind["high"][pos - 2]
    hi0 = ind["high"][pos]
    lo0 = ind["low"][pos]
    if nan(c1, hi1, lo1, lo2, hi2, hi0, lo0):
        return None
    # Buy setup: prior bar naked down close, current bar breaks above prior bar high
    if c1 < lo2 and hi0 > hi1:
        return "long"
    # Sell setup: prior bar naked up close, current bar breaks below prior bar low
    if c1 > hi2 and lo0 < lo1:
        return "short"
    return None
