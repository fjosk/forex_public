#!/usr/bin/env python3
"""ichimoku_chikou_cross_earnforex -- Chikou crosses price with cloud confirmation. EarnForex EA."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_chikou_cross_earnforex",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_a, ich_b, close",
    "long": "Chikou crosses price from below AND close above both Senkou spans",
    "short": "Chikou crosses price from above AND close below both Senkou spans",
    "desc": "Ichimoku Chikou price cross with dual-cloud position confirmation (EarnForex EA)",
    "source": "https://www.earnforex.com/metatrader-expert-advisors/Ichimoku-Chikou-Cross/",
}


def signal(ind, pos, htf=None):
    """Chikou cross price + cloud position confirmation."""
    if pos < 53:
        return None
    c = ind["close"]
    a = ind["ich_a"]
    b = ind["ich_b"]
    # Chikou span = close[pos] placed at bar[pos-26]; price at that bar = close[pos-26]
    chikou_cur = c[pos]
    price_26 = c[pos - 26]
    chikou_prev = c[pos - 1]
    price_27 = c[pos - 27]
    # Cloud at current bar
    a_cur = a[pos]
    b_cur = b[pos]
    if nan(chikou_cur, price_26, chikou_prev, price_27, a_cur, b_cur, c[pos]):
        return None
    chikou_cross_up = chikou_prev <= price_27 and chikou_cur > price_26
    chikou_cross_dn = chikou_prev >= price_27 and chikou_cur < price_26
    cloud_above = c[pos] > a_cur and c[pos] > b_cur
    cloud_below = c[pos] < a_cur and c[pos] < b_cur
    if chikou_cross_up and cloud_above:
        return "long"
    if chikou_cross_dn and cloud_below:
        return "short"
    return None
