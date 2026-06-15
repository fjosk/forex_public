#!/usr/bin/env python3
"""double_bollinger_band_dbb -- Double Bollinger Band zone system via bb_pctb. web:fxacademy.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "double_bollinger_band_dbb",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "bb_pctb",
    "long": "bb_pctb >= 0.75 (price in upper DBB zone)",
    "short": "bb_pctb <= 0.25 (price in lower DBB zone)",
    "desc": "Double Bollinger Band zone system: upper zone = long, lower zone = short (Cliff Wachtel)",
    "source": "web:https://www.fxacademy.com/learn/trading-with-double-bollinger-bands/lessons/dbbs-three-zones-three-rules",
}


def signal(ind, pos, htf=None):
    """DBB zone: bb_pctb >= 0.75 long, <= 0.25 short, 0.25-0.75 neutral."""
    pctb = ind["bb_pctb"][pos]
    if nan(pctb):
        return None
    if pctb >= 0.75:
        return "long"
    if pctb <= 0.25:
        return "short"
    return None
