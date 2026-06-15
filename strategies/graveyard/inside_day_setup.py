#!/usr/bin/env python3
"""inside_day_setup -- Inside bar compression setup: today's high/low contained within the prior
bar; breakout triggered when current bar exits the prior bar's range.
Trade Your Way to Financial Freedom, Appendix II 'Inside Day'."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_day_setup",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high,low,close",
    "long": "inside bar setup (bar-2 contained in bar-3), then bar-1 close > bar-3 high (breakout up)",
    "short": "inside bar setup, then bar-1 close < bar-3 low (breakout down)",
    "desc": "Inside day compression breakout: entry on close breaking the containing bar's range",
    "source": "Trade Your Way to Financial Freedom, Appendix II 'Inside Day'",
}


def signal(ind, pos, htf=None):
    """Inside bar setup at pos-2, breakout entry at current bar."""
    if pos < 2:
        return None
    # bar at pos-2 is the candidate inside bar; bar at pos-3 is the containing bar
    h_contain = ind["high"][pos - 2]   # the containing bar high (prior to inside bar)
    l_contain = ind["low"][pos - 2]    # the containing bar low
    h_inside = ind["high"][pos - 1]    # the inside bar high
    l_inside = ind["low"][pos - 1]     # the inside bar low
    c = ind["close"][pos]              # current bar close (breakout bar)
    if nan(h_contain, l_contain, h_inside, l_inside, c):
        return None
    # Check inside bar: its range is within the containing bar
    if not (h_inside <= h_contain and l_inside >= l_contain):
        return None
    # Breakout: current close exits the containing bar range
    if c > h_contain:
        return "long"
    if c < l_contain:
        return "short"
    return None
