#!/usr/bin/env python3
"""ichimoku_kinko_hyo_system_chikou -- Chikou span cross: close[pos] vs close[pos-26]. mjprater MQL4."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_kinko_hyo_system_chikou",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close",
    "long": "close crosses above close[26] (Chikou span crosses price 26 bars back)",
    "short": "close crosses below close[26]",
    "desc": "Ichimoku Kinko Hyo simplified Chikou span cross (close vs close-26 crossover)",
    "source": "https://www.mql5.com/en/code/16972",
}


def signal(ind, pos, htf=None):
    """Chikou span cross: close vs close-26."""
    if pos < 27:
        return None
    c = ind["close"]
    cur = c[pos]
    lag = c[pos - 26]
    prev = c[pos - 1]
    lag1 = c[pos - 27]
    if nan(cur, lag, prev, lag1):
        return None
    if prev <= lag1 and cur > lag:
        return "long"
    if prev >= lag1 and cur < lag:
        return "short"
    return None
