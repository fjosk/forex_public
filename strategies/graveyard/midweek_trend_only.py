#!/usr/bin/env python3
"""midweek_trend_only -- EMA trend, but only Tue-Thu (skip Monday gap + Friday noise). DoW class."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "midweek_trend_only",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "dow, ema21, ema50, close",
    "long": "Tue-Thu, ema21 crosses above ema50",
    "short": "Tue-Thu, ema21 crosses below ema50",
    "desc": "EMA21/50 trend filtered to mid-week sessions only",
    "source": "session-class:day-of-week (mid-week trend)",
}


def signal(ind, pos, htf=None):
    d = ind["dow"][pos]
    if nan(d) or int(d) not in (1, 2, 3):      # Tue, Wed, Thu
        return None
    e21, e21p = ind["ema21"][pos], ind["ema21"][pos - 1]
    e50, e50p = ind["ema50"][pos], ind["ema50"][pos - 1]
    if nan(e21, e21p, e50, e50p):
        return None
    if _xup(e21, e21p, e50, e50p):
        return "long"
    if _xdn(e21, e21p, e50, e50p):
        return "short"
    return None
