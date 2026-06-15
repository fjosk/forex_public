#!/usr/bin/env python3
"""chandelier_exit -- Chandelier Exit direction flip entry. web:stockcharts.com."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "chandelier_exit",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "chand_dir",
    "long": "chand_dir flips from -1 to +1 (bullish chandelier reversal)",
    "short": "chand_dir flips from +1 to -1 (bearish chandelier reversal)",
    "desc": "Chandelier Exit direction flip: trade every -1/+1 direction change",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit",
}


def signal(ind, pos, htf=None):
    """Chandelier direction flip: -1->+1 = long, +1->-1 = short."""
    cd = ind["chand_dir"][pos]
    cd1 = ind["chand_dir"][pos - 1]
    if nan(cd, cd1):
        return None
    if cd == 1 and cd1 != 1:
        return "long"
    if cd == -1 and cd1 != -1:
        return "short"
    return None
