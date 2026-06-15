#!/usr/bin/env python3
"""false_breakout_fade -- Penetration above Donchian upper then close back inside triggers short fade; mirror for longs. the_new_market_wizards."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "false_breakout_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "dc_up, dc_lo, high, low, close",
    "long": "low penetrates below Donchian lower then close recovers back above Donchian lower (failed downside breakout)",
    "short": "high penetrates above Donchian upper then close falls back below Donchian upper (failed upside breakout)",
    "desc": "False breakout fade: penetration of Donchian channel quickly reversed; fade the failed break",
    "source": "the_new_market_wizards",
}


def signal(ind, pos, htf=None):
    """Failed breakout: bar penetrates Donchian band but closes back inside = fade signal."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    # Use prior bar Donchian to define the range
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, c, dc_up, dc_lo):
        return None
    # Failed upside breakout: high exceeded dc_up but close fell back below it -> fade short
    if h > dc_up and c < dc_up:
        return "short"
    # Failed downside breakout: low broke dc_lo but close recovered above it -> fade long
    if l < dc_lo and c > dc_lo:
        return "long"
    return None
