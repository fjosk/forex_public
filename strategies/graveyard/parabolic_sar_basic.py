#!/usr/bin/env python3
"""parabolic_sar_basic -- PSAR flip trend reversal entry. mql5.com article 15589 (2024)."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_basic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "psar_dir",
    "long": "psar_dir flips from -1 to +1 (SAR moves from above to below price)",
    "short": "psar_dir flips from +1 to -1 (SAR moves from below to above price)",
    "desc": "Parabolic SAR direction flip: enter long on bullish flip, short on bearish flip",
    "source": "mql5.com article 15589 -- Automating Trading Strategies with Parabolic SAR (2024)",
}


def signal(ind, pos, htf=None):
    """Enter on PSAR direction flip between the prior bar and the current bar."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
