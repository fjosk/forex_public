#!/usr/bin/env python3
"""williams_pct_r_ob_os_pure -- Williams %R pure OB/OS fade. MQL5 articles System 1.

Long when willr < -80 (deep oversold). Short when willr > -20 (deep overbought).
No MA filter. Pure zone-entry mean-reversion.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_pct_r_ob_os_pure",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "willr",
    "long": "willr < -80 (deep oversold zone)",
    "short": "willr > -20 (deep overbought zone)",
    "desc": "Williams %R pure OB/OS fade: long oversold, short overbought; no trend filter",
    "source": "web:https://www.mql5.com/en/articles/11142",
}


def signal(ind, pos, htf=None):
    """Williams %R oversold/overbought zone entry."""
    wr = ind["willr"][pos]
    if nan(wr):
        return None
    if wr < -80:
        return "long"
    if wr > -20:
        return "short"
    return None
