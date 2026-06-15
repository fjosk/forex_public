#!/usr/bin/env python3
"""kangaroo_tail_reversal -- One-day spike reversal (kangaroo tail). come_into_my_trading_room_alexander_elder.

Middle bar of 3 has a spike range >= 3x ATR; flanking bars are narrow; current bar confirms reversal
by closing near the base of the spike (opposite side from the tail tip).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "kangaroo_tail_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "high,low,close,open,atr",
    "long": "spike bar (range >= 3*ATR) with long lower extension; next bar (current) closes near spike-bar open (upper portion = base of down tail)",
    "short": "spike bar (range >= 3*ATR) with long upper extension; next bar closes near spike-bar open (lower portion = base of up tail)",
    "desc": "Kangaroo tail: massive spike bar followed by narrow return bar signals exhaustion reversal",
    "source": "come_into_my_trading_room_alexander_elder, Ch5 pp.75-77",
}


def signal(ind, pos, htf=None):
    """Kangaroo tail reversal: spike bar at pos-1, confirmation at pos."""
    if pos < 3:
        return None
    # Spike bar (pos - 1)
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    # Left neighbor (pos - 2)
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    # Current bar (pos) - the confirming bar
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    atr = ind["atr"][pos]
    if nan(h1, l1, o1, c1, h2, l2, h, l, c, atr):
        return None
    spike_range = h1 - l1
    if atr <= 0 or spike_range < 3.0 * atr:
        return None
    # Down-tail (bullish kangaroo): spike bar has long lower extension
    # lower extension = distance from open down to low
    lower_ext = o1 - l1
    upper_ext = h1 - o1
    if lower_ext > upper_ext and lower_ext > 1.5 * atr:
        # Confirmation: current bar closes above midpoint of spike (near the base = upper portion of spike)
        midpoint = (h1 + l1) / 2.0
        if c > midpoint and h < h1:
            return "long"
    # Up-tail (bearish kangaroo): spike bar has long upper extension
    if upper_ext > lower_ext and upper_ext > 1.5 * atr:
        # Confirmation: current bar closes below midpoint of spike
        midpoint = (h1 + l1) / 2.0
        if c < midpoint and l > l1:
            return "short"
    return None
