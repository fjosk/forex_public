#!/usr/bin/env python3
"""parabolic_sar_flip -- PSAR direction flip entry; trail SL with SAR. earnforex.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "parabolic_sar_flip",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir",
    "long": "psar_dir flips from -1 to +1 (SAR moves from above to below price)",
    "short": "psar_dir flips from +1 to -1 (SAR moves from below to above price)",
    "desc": "Pure PSAR direction flip: enter on SAR stop-and-reverse; trail with SAR dots",
    "source": "web:https://www.earnforex.com/forex-strategy/parabolic-sar-strategy/",
}


def signal(ind, pos, htf=None):
    """PSAR direction flip: long on -1->+1, short on +1->-1."""
    pd = ind["psar_dir"][pos]
    pdp = ind["psar_dir"][pos - 1]
    if nan(pd, pdp):
        return None
    if pd == 1 and pdp == -1:
        return "long"
    if pd == -1 and pdp == 1:
        return "short"
    return None
