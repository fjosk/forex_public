#!/usr/bin/env python3
"""range_filter_dw -- Range Filter DW direction flip entry. web:tradingview.com/DonovanWall."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "range_filter_dw",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "rf_dir",
    "long": "rf_dir flips to 1 (price crosses above range filter upper band)",
    "short": "rf_dir flips to -1 (price crosses below range filter lower band)",
    "desc": "Range Filter DW (DonovanWall): trade on rf_dir direction flip",
    "source": "web:https://www.tradingview.com/script/lut7sBgG-Range-Filter-DW/",
}


def signal(ind, pos, htf=None):
    """Range Filter: rf_dir flips from non-1 to 1 = long; from non-(-1) to -1 = short."""
    rd = ind["rf_dir"][pos]
    rd1 = ind["rf_dir"][pos - 1]
    if nan(rd, rd1):
        return None
    if rd == 1 and rd1 != 1:
        return "long"
    if rd == -1 and rd1 != -1:
        return "short"
    return None
