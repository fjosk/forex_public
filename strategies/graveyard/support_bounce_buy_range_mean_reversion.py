#!/usr/bin/env python3
"""support_bounce_buy_range_mean_reversion -- In a sideways range, buy when price touches
Donchian lower support and turns up; sell/short when it touches upper resistance and turns down.

Source: the_naked_trader_how_anyone_can_still_make_money_t, pp.129,146.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "support_bounce_buy_range_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, dc_lo, dc_up, chop",
    "long": "Range regime (chop > 50); low touches dc_lo and close > close[1] (bounce up)",
    "short": "Range regime (chop > 50); high touches dc_up and close < close[1] (turn down)",
    "desc": "Support bounce buy at Donchian lower band with reversal confirmation in range market",
    "source": "the_naked_trader_how_anyone_can_still_make_money_t pp.129,146",
}

_CHOP_THRESH = 50.0


def signal(ind, pos, htf=None):
    """Donchian support/resistance bounce in a range."""
    if pos < 1:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    ch = ind["chop"][pos]
    if nan(c0, c1, lo, hi, dlo, dup, ch) or dup <= dlo:
        return None
    if ch <= _CHOP_THRESH:
        return None
    # bounce off support: low touched dc_lo and close turned up
    if lo <= dlo and c0 > c1:
        return "long"
    # reversal from resistance: high touched dc_up and close turned down
    if hi >= dup and c0 < c1:
        return "short"
    return None
