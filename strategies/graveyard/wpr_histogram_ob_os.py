#!/usr/bin/env python3
"""wpr_histogram_ob_os -- Williams %R enters OB/OS zone (histogram color flip). GODZILLA MQL5 2016.

Long when willr crosses into oversold: willr[pos-1] >= -80 AND willr[pos] < -80.
Short when willr crosses into overbought: willr[pos-1] <= -20 AND willr[pos] > -20.
Models the histogram color-change trigger from the EA.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "wpr_histogram_ob_os",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "willr",
    "long": "willr crosses below -80 (histogram turns blue = entering oversold)",
    "short": "willr crosses above -20 (histogram turns red = entering overbought)",
    "desc": "Williams %R zone entry on OB/OS histogram color flip; Exp_WPR_Histogram EA",
    "source": "web:https://www.mql5.com/en/code/14953",
}


def signal(ind, pos, htf=None):
    """Williams %R crosses into oversold/overbought zone."""
    wr = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(wr, wr1):
        return None
    if wr1 >= -80 and wr < -80:
        return "long"
    if wr1 <= -20 and wr > -20:
        return "short"
    return None
