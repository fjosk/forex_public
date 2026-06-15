#!/usr/bin/env python3
"""williams_r_momentum_cross -- Williams %R Momentum Cross (-50 Threshold).
web:https://github.com/armelf/Financial-Algorithms
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "williams_r_momentum_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "willr",
    "long": "willr crosses above -50 AND 4-bar smoothed willr momentum is positive",
    "short": "willr crosses below -50 AND 4-bar smoothed willr momentum is negative",
    "desc": "Williams %R midpoint (-50) cross with 4-bar momentum filter to avoid whipsaws",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """Williams %R -50 threshold cross gated by 4-bar smoothed first-difference momentum."""
    if pos < 5:
        return None
    wr = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(wr, wr1):
        return None
    # 4-bar SMA of willr first differences
    deltas = []
    for i in range(1, 5):
        wa = ind["willr"][pos - i + 1]
        wb = ind["willr"][pos - i]
        if nan(wa, wb):
            return None
        deltas.append(wa - wb)
    mwr = sum(deltas) / 4.0
    # cross above -50
    if wr > -50 and wr1 <= -50 and mwr > 0:
        return "long"
    # cross below -50
    if wr < -50 and wr1 >= -50 and mwr < 0:
        return "short"
    return None
