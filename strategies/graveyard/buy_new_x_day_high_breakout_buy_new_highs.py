#!/usr/bin/env python3
"""buy_new_x_day_high_breakout -- Buy when today's high exceeds prior X-day highest high; mirror short on new X-day low. long_term_secrets_to_short_term_trading."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "buy_new_x_day_high_breakout_buy_new_highs",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high breaks above prior X-day highest high (Donchian upper)",
    "short": "low breaks below prior X-day lowest low (Donchian lower)",
    "desc": "Buy new X-day high / sell new X-day low Donchian breakout (Truth 2 from Williams)",
    "source": "long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Donchian X-day breakout: buy on new X-day high, sell on new X-day low."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if l < dc_lo:
        return "short"
    return None
