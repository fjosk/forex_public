#!/usr/bin/env python3
"""bollinger_keltner_squeeze_breakout -- BB/KC squeeze release breakout. web:strategy-workspaceegiesresources."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_keltner_squeeze_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "bb_lo, bb_up, bb_width, kc_lo, kc_up, close",
    "long": "BB was inside KC (squeeze), BB_upper crosses above KC_upper, close above bb_up",
    "short": "BB was inside KC (squeeze), BB_lower crosses below KC_lower, close below bb_lo",
    "desc": "Bollinger-Keltner squeeze release breakout: BB expands out of KC with price confirmation",
    "source": "web:https://www.strategy-workspaceegiesresources.com/bollinger-bands-forex-strategies/24-squeeze-breakout/",
}


def signal(ind, pos, htf=None):
    """BB/KC squeeze release breakout."""
    c = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    if nan(c, bb_up, bb_lo, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1):
        return None
    # Prior bar: squeeze was on (BB inside KC)
    squeeze_prev = bb_up1 < kc_up1 and bb_lo1 > kc_lo1
    if not squeeze_prev:
        return None
    # Squeeze releases upward: upper BB now >= upper KC, price confirms
    if bb_up >= kc_up and c > bb_up:
        return "long"
    # Squeeze releases downward: lower BB now <= lower KC, price confirms
    if bb_lo <= kc_lo and c < bb_lo:
        return "short"
    return None
