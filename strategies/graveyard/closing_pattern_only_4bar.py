#!/usr/bin/env python3
"""closing_pattern_only_4bar -- 4-bar close sequence momentum (Davey). Kevin Davey "Entry and Exit Confessions".

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "closing_pattern_only_4bar",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close",
    "long": "close[-1]>close[-3] AND close>close[-2] AND close[-2]>close[-1]",
    "short": "close[-1]<close[-3] AND close<close[-2] AND close[-2]<close[-1]",
    "desc": "4-bar close sequence pattern: stepped close structure signals continuation",
    "source": "Kevin Davey 'Entry and Exit Confessions of a Champion Trader'; zeta-zetra.github.io",
}


def signal(ind, pos, htf=None):
    """4-bar close sequence: stepped close structure signals continuation."""
    if pos < 3:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    c3 = ind["close"][pos - 3]
    if nan(c0, c1, c2, c3):
        return None
    # long: c[-1]>c[-3] AND c[0]>c[-2] AND c[-2]>c[-1]
    if c1 > c3 and c0 > c2 and c2 > c1:
        return "long"
    # short: c[-1]<c[-3] AND c[0]<c[-2] AND c[-2]<c[-1]
    if c1 < c3 and c0 < c2 and c2 < c1:
        return "short"
    return None
