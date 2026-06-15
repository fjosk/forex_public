#!/usr/bin/env python3
"""turtle_system_two_s2_55_day_breakout_entry_20_day_breakout_exit -- Turtle S2: enter on 55-bar
high/low breakout (hh_n/ll_n proxy); no prior-winner filter (always taken).
The Complete TurtleTrader, ch.5 The Rules."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_system_two_s2_55_day_breakout_entry_20_day_breakout_exit",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "hh_n,ll_n,high,low",
    "long": "high breaks above 55-bar highest high (hh_n proxy for 55-day Donchian)",
    "short": "low breaks below 55-bar lowest low (ll_n proxy for 55-day Donchian)",
    "desc": "Turtle S2 55-bar Donchian breakout entry, always taken (no filter)",
    "source": "The Complete TurtleTrader, ch.5 System Two (55-day breakout entry, 20-day exit)",
}


def signal(ind, pos, htf=None):
    """Turtle S2: 55-bar high/low breakout via hh_n/ll_n."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    hh = ind["hh_n"][pos]
    ll = ind["ll_n"][pos]
    if nan(h, l, hh, ll):
        return None
    if h > hh:
        return "long"
    if l < ll:
        return "short"
    return None
