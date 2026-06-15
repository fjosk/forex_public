#!/usr/bin/env python3
"""three_up_days_close_above_prior_high_sell_next_day -- Three-up-day exhaustion short. long_term_secrets_to_short_term_trading.

Setup: three consecutive up closes (close[i]>close[i-1], close[i-1]>close[i-2], close[i-2]>close[i-3])
AND today closes above yesterday's high -> sell (short) signal. Williams: S&P best on Tue->sell Wed.
Signal fires at bar i (current) to sell on bar i's close / next open.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "three_up_days_close_above_prior_high_sell_next_day",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,close",
    "long": "none (spec is short-only exhaustion sell)",
    "short": "Three consecutive up closes AND today close > yesterday high -> exhaustion short",
    "desc": "Three-up-day exhaustion: three consecutive up closes with close above prior high triggers a short",
    "source": "book:long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Three up closes + close above prior high -> exhaustion short."""
    if pos < 3:
        return None
    h = ind["high"]
    c = ind["close"]
    if nan(c[pos], c[pos-1], c[pos-2], c[pos-3], h[pos-1]):
        return None

    three_up = (c[pos] > c[pos-1] and
                c[pos-1] > c[pos-2] and
                c[pos-2] > c[pos-3])
    close_above_prior_high = c[pos] > h[pos-1]

    if three_up and close_above_prior_high:
        return "short"

    return None
