#!/usr/bin/env python3
"""trading_range_fade_with_stop_and_reverse -- Classic range fade: sell near Donchian upper band,
buy near lower band; stop-and-reverse on decisive band penetration.

Source: douglas_mark_the_disciplined_trader_1990_isbn_0132, Ch.15 pp.204-206.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "trading_range_fade_with_stop_and_reverse",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, dc_lo, dc_up, chop, atr",
    "long": "Range (chop > 50); close near dc_lo (within 0.2*ATR): buy just inside support",
    "short": "Range (chop > 50); close near dc_up (within 0.2*ATR): sell just inside resistance",
    "desc": "Trading-range fade: sell near Donchian resistance, buy near support; stop-and-reverse on breakout",
    "source": "douglas_mark_the_disciplined_trader_1990_isbn_0132 Ch.15 pp.204-206",
}

_CHOP_THRESH = 50.0


def signal(ind, pos, htf=None):
    """Range fade at Donchian bands with range-regime filter."""
    c = ind["close"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    ch = ind["chop"][pos]
    a = ind["atr"][pos]
    if nan(c, dlo, dup, ch, a) or a <= 0 or dup <= dlo:
        return None
    if ch <= _CHOP_THRESH:
        return None
    buf = 0.20 * a
    if c <= dlo + buf:
        return "long"
    if c >= dup - buf:
        return "short"
    return None
