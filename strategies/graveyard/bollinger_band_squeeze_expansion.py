#!/usr/bin/env python3
"""bollinger_band_squeeze_expansion -- BB Width squeeze then breakout with MACD histogram confirm. web:highstrike.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_band_squeeze_expansion",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, bb_width, macd_hist, close",
    "long": "bb_width at 60-bar low (squeeze), then close > bb_up with macd_hist > 0",
    "short": "bb_width at 60-bar low (squeeze), then close < bb_lo with macd_hist < 0",
    "desc": "Bollinger Band squeeze-then-expansion breakout with MACD histogram direction confirm",
    "source": "web:https://highstrike.com/bollinger-bands-strategy/",
}

_LOOKBACK = 60


def signal(ind, pos, htf=None):
    """BB squeeze (60-bar bb_width low) then close breaks outside band, MACD hist confirms."""
    cl = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bbw = ind["bb_width"][pos]
    mh = ind["macd_hist"][pos]
    if nan(cl, bb_up, bb_lo, bbw, mh):
        return None
    if pos < _LOOKBACK:
        return None
    # check if prior bar had squeeze (bb_width at N-bar minimum over the window ending at pos-1)
    bbw1 = ind["bb_width"][pos - 1]
    if nan(bbw1):
        return None
    window = ind["bb_width"][pos - _LOOKBACK: pos]
    if len(window) < _LOOKBACK:
        return None
    min_w = float("inf")
    for v in window:
        if v == v and v is not None and v < min_w:
            min_w = v
    squeeze_prev = bbw1 <= min_w
    if not squeeze_prev:
        return None
    if cl > bb_up and mh > 0:
        return "long"
    if cl < bb_lo and mh < 0:
        return "short"
    return None
