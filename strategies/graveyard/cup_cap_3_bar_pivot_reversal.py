#!/usr/bin/env python3
"""cup_cap_3_bar_pivot_reversal -- Cup/Cap 3-bar pivot: center bar of 3 is the local low (cup)
or high (cap); enter on close breaking through center bar extreme.
Kaufman, Trading Systems and Methods, Ch.9 p.227-228."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cup_cap_3_bar_pivot_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,low,close",
    "long": "cap: middle bar has highest high of 3; current close > middle bar high (breakout above cap)",
    "short": "cup: middle bar has lowest low of 3; current close < middle bar low (breakout below cup)",
    "desc": "Cup/Cap 3-bar pivot reversal: break of 3-bar pivot extreme confirms directional move",
    "source": "Kaufman, Trading Systems and Methods, Ch.9 'Cup and Cap' p.227-228",
}


def signal(ind, pos, htf=None):
    """Cap breakout = long; Cup breakout = short. 3-bar pivot geometry."""
    if pos < 3:
        return None
    # pos-1 is the potential pivot (middle bar), pos-2 and pos-3 are flanks
    # We check pos-2 as center of the 3 bars: pos-3, pos-2, pos-1
    h_left = ind["high"][pos - 3]
    h_mid = ind["high"][pos - 2]
    h_right = ind["high"][pos - 1]
    l_left = ind["low"][pos - 3]
    l_mid = ind["low"][pos - 2]
    l_right = ind["low"][pos - 1]
    c = ind["close"][pos]
    if nan(h_left, h_mid, h_right, l_left, l_mid, l_right, c):
        return None
    # Cap: center bar is the highest high -> confirm long on close above it
    if h_mid >= h_left and h_mid >= h_right and c > h_mid:
        return "long"
    # Cup: center bar is the lowest low -> confirm short on close below it
    if l_mid <= l_left and l_mid <= l_right and c < l_mid:
        return "short"
    return None
