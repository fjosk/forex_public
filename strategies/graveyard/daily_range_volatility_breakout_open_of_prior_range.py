#!/usr/bin/env python3
"""daily_range_volatility_breakout_from_open -- Buy at open + 100% prior range, sell at open - 100% prior range. long_term_secrets_to_short_term_trading."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "daily_range_volatility_breakout_open_of_prior_range",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "open, high, low, prev_dhh, prev_dll",
    "long": "high >= today's open + 100% of prior day range",
    "short": "low <= today's open - 100% of prior day range",
    "desc": "Daily range volatility breakout: open +/- 100% of yesterday's range as buy/sell triggers",
    "source": "long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Open + k * prior_range breakout trigger."""
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
    buy_trigger = o + 1.0 * prior_range
    sell_trigger = o - 1.0 * prior_range
    if h >= buy_trigger:
        return "long"
    if l <= sell_trigger:
        return "short"
    return None
