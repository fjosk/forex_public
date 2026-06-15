#!/usr/bin/env python3
"""keltner_bb_squeeze_breakout -- TTM-style KC-BB squeeze breakout with MACD histogram confirm. web:traderspost.io."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "keltner_bb_squeeze_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, kc_up, kc_lo, macd_hist",
    "long": "BB inside KC (squeeze on prior bar), upper BB breaks above upper KC, macd_hist > 0",
    "short": "BB inside KC (squeeze on prior bar), lower BB breaks below lower KC, macd_hist < 0",
    "desc": "TTM-style Keltner-Bollinger squeeze breakout with MACD histogram direction confirm",
    "source": "web:https://blog.traderspost.io/article/keltner-channel-trading-strategies",
}


def signal(ind, pos, htf=None):
    """KC-BB squeeze fires when BB expands outside KC; MACD hist confirms direction."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    mh = ind["macd_hist"][pos]
    if nan(bb_up, bb_lo, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1, mh):
        return None
    squeeze_prev = bb_up1 < kc_up1 and bb_lo1 > kc_lo1
    if not squeeze_prev:
        return None
    if bb_up >= kc_up and mh > 0:
        return "long"
    if bb_lo <= kc_lo and mh < 0:
        return "short"
    return None
