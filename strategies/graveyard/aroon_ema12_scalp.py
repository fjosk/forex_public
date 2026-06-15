#!/usr/bin/env python3
"""aroon_ema12_scalp -- Aroon Oscillator direction + EMA8/EMA13 rainbow cross. web:fxtsp.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "aroon_ema12_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "aroon_osc, ema8, ema13 (proxy ema12)",
    "long": "aroon_osc > 0 AND ema8 crosses above ema13 with close > ema13",
    "short": "aroon_osc < 0 AND ema8 crosses below ema13 with close < ema13",
    "desc": "Aroon Oscillator direction filter with EMA8/13 rainbow cross entry scalp",
    "source": "web:https://www.fxtsp.com/aroon-rainbow-forex-scalping-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Aroon oscillator direction with fast/slow EMA cross confirmation."""
    aroon = ind["aroon_osc"][pos]
    e8 = ind["ema8"][pos]
    e8p = ind["ema8"][pos - 1]
    e13 = ind["ema13"][pos]
    e13p = ind["ema13"][pos - 1]
    c = ind["close"][pos]
    if nan(aroon, e8, e8p, e13, e13p, c):
        return None
    if aroon > 0 and _xup(e8, e8p, e13, e13p) and c > e13:
        return "long"
    if aroon < 0 and _xdn(e8, e8p, e13, e13p) and c < e13:
        return "short"
    return None
