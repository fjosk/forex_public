#!/usr/bin/env python3
"""turtle_price_channel_breakout -- Turtle System 1/2 Donchian EA. TFMT4 price-channels."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_price_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, hh_n, ll_n, atr",
    "long": "close > dc_up (N-bar Donchian high)",
    "short": "close < dc_lo (N-bar Donchian low)",
    "desc": "Turtle price-channel EA: Donchian breakout entry with hh_n/ll_n exit approximation",
    "source": "web:http://www.tfmt4.com/price-channels.html",
}


def signal(ind, pos, htf=None):
    """Donchian breakout; hh_n/ll_n available for exit but engine handles exit via BREAK preset."""
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    atr = ind["atr"][pos]
    if nan(c, dc_up, dc_lo, atr):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
