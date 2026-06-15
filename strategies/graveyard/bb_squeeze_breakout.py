#!/usr/bin/env python3
"""bb_squeeze_breakout -- BB squeeze then close outside band with body filter. web:sahi.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bb_squeeze_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "5m",
    "indicators": "bb_up, bb_lo, bbw_pct",
    "long": "squeeze >= 5 bars then close > bb_up with body >= 60% of range",
    "short": "squeeze >= 5 bars then close < bb_lo with body >= 60% of range",
    "desc": "Bollinger Band squeeze breakout: low-volatility pinch then close outside band",
    "source": "web:https://www.sahi.com/blogs/bollinger-bands-scalping-squeeze-breakouts-and-mean-reversion-setups",
}


def signal(ind, pos, htf=None):
    """Trade the expansion after at least 5 consecutive squeeze bars."""
    if pos < 6:
        return None
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bbw = ind["bbw_pct"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(bb_up, bb_lo, bbw, c, o, h, lo):
        return None
    bar_range = h - lo
    if bar_range <= 0:
        return None
    body_pct = abs(c - o) / bar_range
    # count consecutive squeeze bars (bbw_pct below 25th percentile of last 50 bars)
    hist = ind["bbw_pct"][max(0, pos - 50):pos]
    if len(hist) < 10:
        return None
    threshold = sorted(hist)[len(hist) // 4]
    squeeze_count = 0
    for i in range(1, min(21, pos)):
        if ind["bbw_pct"][pos - i] < threshold:
            squeeze_count += 1
        else:
            break
    if squeeze_count < 5:
        return None
    if c > bb_up and body_pct >= 0.60:
        return "long"
    if c < bb_lo and body_pct >= 0.60:
        return "short"
    return None
