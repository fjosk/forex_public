#!/usr/bin/env python3
"""psar_direction_flip -- Parabolic SAR direction flip entry (stop-and-reverse). fmzquant/strategies GitHub."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "psar_direction_flip",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "psar_dir",
    "long": "psar_dir flips from -1 to +1 (SAR drops below price)",
    "short": "psar_dir flips from +1 to -1 (SAR rises above price)",
    "desc": "Parabolic SAR direction flip entry (stop-and-reverse)",
    "source": "fmzquant/strategies GitHub; J. Welles Wilder SAR (1978)",
}


def signal(ind, pos, htf=None):
    """Enter on PSAR direction flip; opposite flip exits and reverses."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
