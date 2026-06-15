#!/usr/bin/env python3
"""moving_average_ribbon_position -- EMA20/50/200 ribbon alignment position trade. web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/moving-average-ribbon"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "moving_average_ribbon_position",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ema20, ema50, ema200, close",
    "long": "ema20 > ema50 > ema200 AND ribbon expanding AND close > ema20",
    "short": "ema20 < ema50 < ema200 AND ribbon expanding downward AND close < ema20",
    "desc": "MA ribbon position trade: three-EMA alignment with gap expansion entry",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/moving-average-ribbon",
}


def signal(ind, pos, htf=None):
    """Ribbon aligned and expanding -- enter in trend direction."""
    if pos < 5:
        return None
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    e20_5 = ind["ema20"][pos - 5]
    e200_5 = ind["ema200"][pos - 5]
    c = ind["close"][pos]
    if nan(e20, e50, e200, e20_5, e200_5, c):
        return None
    aligned_up = e20 > e50 and e50 > e200
    aligned_dn = e20 < e50 and e50 < e200
    expanding_up = (e20 - e200) > (e20_5 - e200_5)
    expanding_dn = (e200 - e20) > (e200_5 - e20_5)
    if aligned_up and expanding_up and c > e20:
        return "long"
    if aligned_dn and expanding_dn and c < e20:
        return "short"
    return None
