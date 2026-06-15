#!/usr/bin/env python3
"""prior_day_hl_breakout -- Prior-day high/low stop-run breakout (stop-hunting setup).
the_new_market_wizards (Monroe Trout).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "prior_day_hl_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "prev_dhh, prev_dll, high, low",
    "long": "high breaks above prior-day high (triggers stop cluster above PDH -> long)",
    "short": "low breaks below prior-day low (triggers stop cluster below PDL -> short)",
    "desc": "Prior-day high/low stop-run: breakout of PDH or PDL anticipates stop-triggered acceleration",
    "source": "book: the_new_market_wizards (Monroe Trout chapter)",
}


def signal(ind, pos, htf=None):
    """Long on break of prior-day high; short on break of prior-day low."""
    h = ind["high"][pos]
    lo = ind["low"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    if nan(h, lo, pdh, pdl):
        return None
    if h > pdh:
        return "long"
    if lo < pdl:
        return "short"
    return None
