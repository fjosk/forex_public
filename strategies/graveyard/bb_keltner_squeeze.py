#!/usr/bin/env python3
"""bb_keltner_squeeze -- Bollinger-Keltner squeeze breakout (BB inside KC release). hasnocool TTM Squeeze.

Squeeze is active when BB bands are fully inside the Keltner channel. When the squeeze releases
(BB bands re-expand outside KC), enter in the direction the close is relative to BB mid. Exits via
BREAK archetype (trend + time stop).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bb_keltner_squeeze",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, bb_mid, kc_up, kc_lo",
    "long": "squeeze releases (BB was inside KC) AND close > bb_mid",
    "short": "squeeze releases AND close < bb_mid",
    "desc": "BB-Keltner squeeze: enter on volatility expansion in the direction of close vs BB midline",
    "source": "https://github.com/hasnocool/tradingview-pine-scripts (BB Keltner Squeeze Strategy)",
}


def signal(ind, pos, htf=None):
    """BB-Keltner squeeze release breakout."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_mid = ind["bb_mid"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    c = ind["close"][pos]
    if nan(bb_up, bb_lo, bb_mid, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1, c):
        return None
    # Squeeze on previous bar: BB inside KC
    was_squeeze = (bb_up1 < kc_up1) and (bb_lo1 > kc_lo1)
    if not was_squeeze:
        return None
    # Squeeze release on current bar
    squeeze_now = (bb_up < kc_up) and (bb_lo > kc_lo)
    if squeeze_now:
        return None
    if c > bb_mid:
        return "long"
    if c < bb_mid:
        return "short"
    return None
