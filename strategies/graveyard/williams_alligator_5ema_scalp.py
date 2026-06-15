#!/usr/bin/env python3
"""williams_alligator_5ema_scalp -- Williams Alligator fanning + EMA5 cross scalp.

Long:  Alligator lines fan upward (jaw < teeth < lips), close above all lines,
       ema5 crosses above al_jaw (jaw is the lowest line).
Short: lines fan downward (jaw > teeth > lips), close below all lines,
       ema5 crosses below al_jaw (jaw is the highest line).
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "williams_alligator_5ema_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "al_jaw, al_teeth, al_lips, ema5",
    "long": "Alligator fanning up (jaw < teeth < lips), close > al_lips, ema5 crosses above al_jaw",
    "short": "Alligator fanning down (jaw > teeth > lips), close < al_lips, ema5 crosses below al_jaw",
    "desc": "Williams Alligator fanning lines + EMA5 cross scalp",
    "source": "web:https://www.fmz.com/lang/en/strategy/427811",
}


def signal(ind, pos, htf=None):
    """Williams Alligator + EMA5 cross scalp."""
    jaw0 = ind["al_jaw"][pos];   jaw1 = ind["al_jaw"][pos - 1]
    tth0 = ind["al_teeth"][pos]
    lip0 = ind["al_lips"][pos]
    e50 = ind["ema5"][pos];      e51 = ind["ema5"][pos - 1]
    c = ind["close"][pos]
    if nan(jaw0, jaw1, tth0, lip0, e50, e51, c):
        return None

    bull_fan = jaw0 < tth0 < lip0 and c > lip0
    bear_fan = jaw0 > tth0 > lip0 and c < lip0

    ema_cross_up = _xup(e50, e51, jaw0, jaw1)
    ema_cross_dn = _xdn(e50, e51, jaw0, jaw1)

    if bull_fan and ema_cross_up:
        return "long"
    if bear_fan and ema_cross_dn:
        return "short"
    return None
