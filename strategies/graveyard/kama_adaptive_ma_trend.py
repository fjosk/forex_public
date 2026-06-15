#!/usr/bin/env python3
"""kama_adaptive_ma_trend -- KAMA slope turn trend entry. web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/kaufmans-adaptive-moving-average-kama"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kama_adaptive_ma_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "kama, close",
    "long": "KAMA slope turns positive (was flat/negative) AND close > kama",
    "short": "KAMA slope turns negative AND close < kama",
    "desc": "KAMA slope reversal entry: adaptive MA turns from flat to trending",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/kaufmans-adaptive-moving-average-kama",
}


def signal(ind, pos, htf=None):
    """KAMA slope turns from non-rising to rising (or non-falling to falling)."""
    kama = ind["kama"][pos]
    kama1 = ind["kama"][pos - 1]
    kama2 = ind["kama"][pos - 2] if pos >= 2 else None
    c = ind["close"][pos]
    if nan(kama, kama1, c):
        return None
    kama_rising = kama > kama1
    kama_falling = kama < kama1
    # require slope turn: rising now but was not rising before
    if pos >= 2 and not nan(kama2):
        was_rising = kama1 > kama2
        was_falling = kama1 < kama2
        turn_up = kama_rising and not was_rising
        turn_dn = kama_falling and not was_falling
    else:
        turn_up = kama_rising
        turn_dn = kama_falling
    if turn_up and c > kama:
        return "long"
    if turn_dn and c < kama:
        return "short"
    return None
