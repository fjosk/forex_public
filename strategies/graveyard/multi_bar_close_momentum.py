#!/usr/bin/env python3
"""multi_bar_close_momentum -- Multi-bar close acceleration: 4-condition sequential close structure.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "multi_bar_close_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "close",
    "long": "close[-1]>close[-3] AND close>close[-2] AND close[-2]>close[-1] AND close>close[-1]",
    "short": "mirror: sequential lower closes with acceleration",
    "desc": "Multi-bar close acceleration: 4-condition sequential close structure signals accelerating momentum",
    "source": "github.com/zeta-zetra/code combination_3.py",
}


def signal(ind, pos, htf=None):
    """Multi-bar close acceleration momentum."""
    if pos < 3:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    c3 = ind["close"][pos - 3]
    if nan(c0, c1, c2, c3):
        return None
    # long: c[-1]>c[-3] AND c>c[-2] AND c[-2]>c[-1] AND c>c[-1]
    if c1 > c3 and c0 > c2 and c2 > c1 and c0 > c1:
        return "long"
    # short: c[-1]<c[-3] AND c<c[-2] AND c[-2]<c[-1] AND c<c[-1]
    if c1 < c3 and c0 < c2 and c2 < c1 and c0 < c1:
        return "short"
    return None
