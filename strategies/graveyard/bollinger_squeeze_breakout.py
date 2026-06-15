#!/usr/bin/env python3
"""bollinger_squeeze_breakout -- BB squeeze breakout with SMA200 trend filter. web:technical-analysis-pro."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_squeeze_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "bb_up, bb_lo, bbw_pct, sma200, close",
    "long": "BB width at low percentile (squeeze), close breaks above bb_up, close above sma200",
    "short": "BB squeeze, close breaks below bb_lo, close below sma200",
    "desc": "Bollinger Band squeeze breakout confirmed by SMA200 trend direction",
    "source": "web:https://www.technical-analysis-pro.com/strategies-bollinger-bands-squeeze-strategy/",
}

_SQUEEZE_PCT = 20.0  # bottom 20th percentile of recent band width


def signal(ind, pos, htf=None):
    """BB squeeze breakout with SMA200 trend filter."""
    c = ind["close"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bbw_pct = ind["bbw_pct"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, bb_up, bb_lo, bbw_pct, s200):
        return None
    squeeze = bbw_pct <= _SQUEEZE_PCT
    if not squeeze:
        return None
    if c > bb_up and c > s200:
        return "long"
    if c < bb_lo and c < s200:
        return "short"
    return None
