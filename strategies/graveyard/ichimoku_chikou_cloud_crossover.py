#!/usr/bin/env python3
"""ichimoku_chikou_cloud_crossover -- Chikou span transitions above/below Ichimoku cloud. QuantConnect."""
from strategies._common import nan, TREND, ALL_CLASSES

# Chikou span = close plotted 26 bars back; read as close[pos-26] vs the cloud at that time.

META = {
    "id": "ichimoku_chikou_cloud_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ich_a, ich_b, close",
    "long": "Chikou span (close[-26]) transitions from inside/below cloud to above cloud",
    "short": "Chikou span transitions from inside/above cloud to below cloud",
    "desc": "Ichimoku Chikou cloud crossover: lagging span location transition signals trend",
    "source": "https://www.quantconnect.com/learning/articles/investment-strategy-library/ichimoku-clouds-in-the-energy-sector",
}


def _get_location(chikou, a, b):
    cloud_top = max(a, b)
    cloud_bot = min(a, b)
    if chikou > cloud_top:
        return 1
    if chikou < cloud_bot:
        return -1
    return 0


def signal(ind, pos, htf=None):
    """Chikou span cloud location transition."""
    if pos < 27:
        return None
    c = ind["close"]
    a = ind["ich_a"]
    b = ind["ich_b"]
    chikou_cur = c[pos - 26]
    chikou_prev = c[pos - 27]
    a_cur = a[pos - 26]
    b_cur = b[pos - 26]
    a_prev = a[pos - 27]
    b_prev = b[pos - 27]
    if nan(chikou_cur, chikou_prev, a_cur, b_cur, a_prev, b_prev):
        return None
    cur_loc = _get_location(chikou_cur, a_cur, b_cur)
    prev_loc = _get_location(chikou_prev, a_prev, b_prev)
    if cur_loc != prev_loc:
        if cur_loc == 1:
            return "long"
        if cur_loc == -1:
            return "short"
    return None
