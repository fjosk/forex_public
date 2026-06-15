#!/usr/bin/env python3
"""waddah_attar_explosion -- Waddah Attar Explosion: MACD momentum vs BB-width explosion line. web:pineify.app."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "waddah_attar_explosion",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "macd_hist, bb_width, atr",
    "long": "macd_hist > 0, rising, > bb_width (explosion line) and > 3.7*atr (dead zone)",
    "short": "abs(macd_hist) < 0, falling, > bb_width and > 3.7*atr",
    "desc": "Waddah Attar Explosion: directional MACD momentum clears BB-width explosion line and ATR dead zone",
    "source": "web:https://pineify.app/resources/blog/waddah-attar-explosion-indicator-tradingview-pine-script",
}


def signal(ind, pos, htf=None):
    """WAE approximation: macd_hist vs bb_width explosion and ATR dead zone."""
    mh = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    bbw = ind["bb_width"][pos]
    atr = ind["atr"][pos]
    if nan(mh, mh1, bbw, atr):
        return None
    dead_zone = 3.7 * atr
    if mh > 0:
        green = mh
        green1 = mh1 if mh1 is not None and mh1 == mh1 and mh1 > 0 else 0.0
        if green > bbw and green > dead_zone and green > green1:
            return "long"
    elif mh < 0:
        red = -mh
        red1 = (-mh1) if mh1 is not None and mh1 == mh1 and mh1 < 0 else 0.0
        if red > bbw and red > dead_zone and red > red1:
            return "short"
    return None
