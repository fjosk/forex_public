#!/usr/bin/env python3
"""week52_breakout_buy -- 52-week (yr_high) Donchian close breakout; long-only. the_naked_trader."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "52_week_breakout_buy",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "yr_high, close",
    "long": "close exceeds the trailing 52-week highest high (yr_high)",
    "short": "no short side",
    "desc": "52-week range breakout long-only on close above annual high",
    "source": "the_naked_trader_how_anyone_can_still_make_money_t",
}


def signal(ind, pos, htf=None):
    """Long when close breaks above the 52-week high."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    yh = ind["yr_high"][pos - 1]
    if nan(c, yh):
        return None
    if c > yh:
        return "long"
    return None
