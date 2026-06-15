#!/usr/bin/env python3
"""bollinger_band_squeeze_breakout -- BB squeeze breakout (width at N-bar minimum). web:howtotrade."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_band_squeeze_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, bb_width, close",
    "long": "BB width at N-bar minimum (squeeze), close breaks above bb_up",
    "short": "BB squeeze, close breaks below bb_lo",
    "desc": "Bollinger Band squeeze breakout: width at rolling minimum then price exits the band",
    "source": "web:https://howtotrade.com/wp-content/uploads/2024/01/Bollinger-Bands-Trading-Strategy.pdf",
}

_SQ_WINDOW = 20  # bars to compute the rolling minimum of bb_width


def signal(ind, pos, htf=None):
    """BB squeeze breakout."""
    c = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_w = ind["bb_width"][pos]
    if nan(c, bb_up, bb_lo, bb_w):
        return None
    if pos < _SQ_WINDOW:
        return None
    # Check that current bb_width is a new N-bar minimum (squeeze condition)
    squeeze = True
    for i in range(pos - _SQ_WINDOW, pos):
        w_i = ind["bb_width"][i]
        if nan(w_i):
            squeeze = False
            break
        if w_i < bb_w:
            squeeze = False
            break
    if not squeeze:
        return None
    if c > bb_up:
        return "long"
    if c < bb_lo:
        return "short"
    return None
