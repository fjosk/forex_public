#!/usr/bin/env python3
"""bb_squeeze_keltner_7candle -- BB squeeze inside KC; enter on release breakout. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bb_squeeze_keltner_7candle",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "bb_lo, bb_up, kc_lo, kc_up, close",
    "long": "BB inside KC (squeeze), then upper BB breaks above upper KC and close > bb_up",
    "short": "BB inside KC (squeeze), then lower BB breaks below lower KC and close < bb_lo",
    "desc": "Bollinger Band squeeze inside Keltner Channel; enter on squeeze release breakout",
    "source": "web:https://www.strategy-workspaceegiesresources.com/bollinger-bands-forex-strategies/24-squeeze-breakout/",
}


def signal(ind, pos, htf=None):
    """BB-KC squeeze: fires when BB releases from inside KC in the breakout direction."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    cl = ind["close"][pos]
    if nan(bb_up, bb_lo, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1, cl):
        return None
    # squeeze was active on the previous bar
    squeeze_prev = bb_up1 < kc_up1 and bb_lo1 > kc_lo1
    if not squeeze_prev:
        return None
    # breakout upward: upper BB crosses above upper KC
    if bb_up >= kc_up and cl > bb_up:
        return "long"
    # breakout downward: lower BB crosses below lower KC
    if bb_lo <= kc_lo and cl < bb_lo:
        return "short"
    return None
