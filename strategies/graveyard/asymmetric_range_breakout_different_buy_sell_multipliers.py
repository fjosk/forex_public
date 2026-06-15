#!/usr/bin/env python3
"""asymmetric_range_breakout -- Open + 40% prior range for longs, open - 200% for shorts. long_term_secrets_to_short_term_trading."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "asymmetric_range_breakout_different_buy_sell_multipliers",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "open, high, low, prev_dhh, prev_dll",
    "long": "high >= open + 0.40 * prior_day_range",
    "short": "low <= open - 2.00 * prior_day_range",
    "desc": "Asymmetric range breakout: tight 40% buy threshold, wide 200% sell threshold relative to prior day range",
    "source": "long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Asymmetric breakout from today's open using yesterday's range as the volatility unit."""
    if pos < 2:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    ph = ind["prev_dhh"][pos]
    pl = ind["prev_dll"][pos]
    if nan(o, h, l, ph, pl):
        return None
    prior_range = ph - pl
    if prior_range <= 0:
        return None
    buy_trigger = o + 0.40 * prior_range
    sell_trigger = o - 2.00 * prior_range
    if h >= buy_trigger:
        return "long"
    if l <= sell_trigger:
        return "short"
    return None
