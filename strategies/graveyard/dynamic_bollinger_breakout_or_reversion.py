#!/usr/bin/env python3
"""dynamic_bollinger_breakout_or_reversion -- BB width squeeze + breakout above/below band. QuantConnect / QC forum.

When BB width is compressed (bbw_pct < 0.20), the first close outside the upper or lower band
signals a breakout entry. The exit archetype is BREAK (ATR trailing stop).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "dynamic_bollinger_breakout_or_reversion",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "bb_up, bb_lo, bb_mid, bbw_pct, close, atr",
    "long": "bbw_pct < 0.20 (squeeze) AND close > bb_up (breakout above upper band)",
    "short": "bbw_pct < 0.20 AND close < bb_lo (breakout below lower band)",
    "desc": "Bollinger Band squeeze breakout: enter first close outside band after BB width compression",
    "source": "https://www.quantconnect.com/forum/discussion/5662/ (QC BB Width Breakout)",
}

_SQUEEZE_THRESH = 0.20


def signal(ind, pos, htf=None):
    """BB squeeze gate + breakout entry."""
    bwp = ind["bbw_pct"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    c = ind["close"][pos]
    if nan(bwp, bb_up, bb_lo, c):
        return None
    if bwp >= _SQUEEZE_THRESH:
        return None
    if c > bb_up:
        return "long"
    if c < bb_lo:
        return "short"
    return None
