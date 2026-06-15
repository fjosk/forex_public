#!/usr/bin/env python3
"""new_highs_new_lows_extreme -- N-year high/low extreme breakout with trend-follow.
alpha_trading_kaufman.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "new_highs_new_lows_extreme",
    "cadences": ["swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "yr_high, yr_low, close",
    "long": "close >= yr_high (new 52-week high) -> ride the momentum",
    "short": "close <= yr_low (new 52-week low) -> ride the decline",
    "desc": "New 52-week extreme breakout; chandelier trail exits",
    "source": "book: alpha_trading_profitable_strategies_that_remove_di",
}


def signal(ind, pos, htf=None):
    """Close at or above yr_high -> long; at or below yr_low -> short."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    yh = ind["yr_high"][pos - 1]
    yl = ind["yr_low"][pos - 1]
    if nan(c, yh, yl):
        return None
    if c >= yh:
        return "long"
    if c <= yl:
        return "short"
    return None
