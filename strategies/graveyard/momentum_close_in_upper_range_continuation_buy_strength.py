#!/usr/bin/env python3
"""momentum_close_in_upper_range_continuation_buy_strength -- Close in upper 65% of bar range
-> buy strength (momentum continuation); close in lower 35% -> short weakness.

Source: long_term_secrets_to_short_term_trading, Ch.15 Truth 1 pp.238-239.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "momentum_close_in_upper_range_continuation_buy_strength",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, high, low",
    "long": "(close - low) / (high - low) >= 0.65: close in upper 65% of bar range -> buy strength",
    "short": "(close - low) / (high - low) <= 0.35: close in lower 35% of bar range -> sell weakness",
    "desc": "Buy strength (close in top 65% of range) or sell weakness (close in bottom 35%) for momentum continuation",
    "source": "long_term_secrets_to_short_term_trading Ch.15 Truth 1 pp.238-239",
}


def signal(ind, pos, htf=None):
    """Range-position momentum: upper 65% = long, lower 35% = short."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(c, h, lo):
        return None
    bar_range = h - lo
    if bar_range <= 0:
        return None
    rng_pct = (c - lo) / bar_range
    if rng_pct >= 0.65:
        return "long"
    if rng_pct <= 0.35:
        return "short"
    return None
