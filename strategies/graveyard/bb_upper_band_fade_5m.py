#!/usr/bin/env python3
"""bb_upper_band_fade_5m -- Re-entry after close back inside BB after an overshoot. web:forextraders.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_upper_band_fade_5m",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "bb_up, bb_lo",
    "long": "prev close < bb_lo, current close > bb_lo with bullish candle (re-entry)",
    "short": "prev close > bb_up, current close < bb_up with bearish candle (re-entry)",
    "desc": "BB band re-entry fade: close back inside the band after an overshoot",
    "source": "web:https://forextraders.com/forex-education/forex-scalping/simple-1-5-and-15-minute-forex-scalping-strategies/",
}


def signal(ind, pos, htf=None):
    """Trade the re-entry candle after price overshoots a Bollinger Band."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up_p = ind["bb_up"][pos - 1]
    bb_lo_p = ind["bb_lo"][pos - 1]
    c = ind["close"][pos]
    c_p = ind["close"][pos - 1]
    o = ind["open"][pos]
    if nan(bb_up, bb_lo, bb_up_p, bb_lo_p, c, c_p, o):
        return None
    # long: previous close below lower band, current close back above it (bullish)
    if c_p < bb_lo_p and c > bb_lo and c > o:
        return "long"
    # short: previous close above upper band, current close back below it (bearish)
    if c_p > bb_up_p and c < bb_up and c < o:
        return "short"
    return None
