#!/usr/bin/env python3
"""bollinger_band_squeeze -- BB bandwidth squeeze breakout (6-month low then close outside band). web:stockcharts.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_band_squeeze",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, bb_width, close",
    "long": "bb_width at 125-bar low (squeeze) on prior bar, then close > bb_up",
    "short": "bb_width at 125-bar low (squeeze) on prior bar, then close < bb_lo",
    "desc": "Bollinger Band squeeze breakout: bandwidth at 6-month low then close breaks outside band",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/bollinger-band-squeeze",
}

_LOOKBACK = 125


def signal(ind, pos, htf=None):
    """BB bandwidth squeeze (125-bar low on prior bar) then breakout close."""
    cl = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    if nan(cl, bb_up, bb_lo):
        return None
    if pos < _LOOKBACK + 1:
        return None
    bbw1 = ind["bb_width"][pos - 1]
    if nan(bbw1):
        return None
    window = ind["bb_width"][pos - _LOOKBACK: pos - 1]
    if len(window) < _LOOKBACK - 1:
        return None
    min_w = float("inf")
    for v in window:
        if v == v and v is not None and v < min_w:
            min_w = v
    squeeze_prev = bbw1 <= min_w
    if not squeeze_prev:
        return None
    if cl > bb_up:
        return "long"
    if cl < bb_lo:
        return "short"
    return None
