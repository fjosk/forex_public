#!/usr/bin/env python3
"""keltner_channel_bollinger_squeeze -- BB-KC squeeze breakout with 5-bar momentum filter. Nikhil-Adithyan / John Carter.

Squeeze exists when BB is inside KC. When squeeze ends, enter in the direction of recent 5-bar
momentum (close vs close 5 bars ago). Mirrors John Carter's TTM Squeeze concept.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "keltner_channel_bollinger_squeeze",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "bb_up, bb_lo, bb_mid, kc_up, kc_lo, kc_mid, close",
    "long": "squeeze releases AND close > close[pos-5] (positive 5-bar momentum)",
    "short": "squeeze releases AND close < close[pos-5] (negative 5-bar momentum)",
    "desc": "Keltner-Bollinger squeeze: enter on BB-KC release in direction of 5-bar momentum",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python; John Carter TTM Squeeze",
}

_MOM_BARS = 5


def signal(ind, pos, htf=None):
    """BB-KC squeeze release with 5-bar momentum direction."""
    if pos < _MOM_BARS + 1:
        return None
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    c = ind["close"][pos]
    c_back = ind["close"][pos - _MOM_BARS]
    if nan(bb_up, bb_lo, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1, c, c_back):
        return None
    # Previous bar must have been in squeeze
    was_squeeze = (bb_up1 < kc_up1) and (bb_lo1 > kc_lo1)
    if not was_squeeze:
        return None
    # Current bar: squeeze must have ended
    in_squeeze = (bb_up < kc_up) and (bb_lo > kc_lo)
    if in_squeeze:
        return None
    momentum = c - c_back
    if momentum > 0:
        return "long"
    if momentum < 0:
        return "short"
    return None
