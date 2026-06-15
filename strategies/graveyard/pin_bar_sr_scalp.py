#!/usr/bin/env python3
"""pin_bar_sr_scalp -- Pin bar geometry at pivot support/resistance. web:priceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_sr_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "15m",
    "indicators": "piv_s1, piv_r1, piv_p, high, low, open, close",
    "long": "bullish pin bar (lower shadow >= 2/3 range, body < 1/3) at piv_s1 or piv_p",
    "short": "bearish pin bar (upper shadow >= 2/3 range, body < 1/3) at piv_r1 or piv_p",
    "desc": "Pin bar reversal at daily pivot support/resistance levels",
    "source": "web:https://priceaction.com/price-action-university/strategies/pin-bar/",
}


def signal(ind, pos, htf=None):
    """Detect pin bar geometry and check if the tail is at a key pivot level."""
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    piv_s1 = ind["piv_s1"][pos]
    piv_r1 = ind["piv_r1"][pos]
    piv_p = ind["piv_p"][pos]
    if nan(h, lo, c, o, piv_s1, piv_r1, piv_p):
        return None
    total_range = h - lo
    if total_range <= 0:
        return None
    body = abs(c - o)
    lower_shadow = (min(c, o) - lo)
    upper_shadow = (h - max(c, o))
    bull_pin = lower_shadow >= 0.66 * total_range and body < 0.33 * total_range
    bear_pin = upper_shadow >= 0.66 * total_range and body < 0.33 * total_range
    pip = 0.0010
    near_support = abs(lo - piv_s1) < pip or abs(lo - piv_p) < pip
    near_resist = abs(h - piv_r1) < pip or abs(h - piv_p) < pip
    if bull_pin and near_support:
        return "long"
    if bear_pin and near_resist:
        return "short"
    return None
