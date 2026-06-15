#!/usr/bin/env python3
"""camarilla_pivot_swing -- Camarilla H4/L4 breakout swing. web:admiralmarkets.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "camarilla_pivot_swing",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "cam_r4, cam_s4, close",
    "long": "close breaks above Camarilla H4 (cam_r4) -- bullish extreme breakout",
    "short": "close breaks below Camarilla L4 (cam_s4) -- bearish extreme breakout",
    "desc": "Camarilla R4/S4 breakout swing entry",
    "source": "web:https://admiralmarkets.com/education/articles/forex-indicators/pivot-point-trading-identifying-support-and-resistance-levels-with-a-pivot-point-indicator",
}


def signal(ind, pos, htf=None):
    """Camarilla H4/L4 breakout."""
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    r4, r4_1 = ind["cam_r4"][pos], ind["cam_r4"][pos - 1]
    s4, s4_1 = ind["cam_s4"][pos], ind["cam_s4"][pos - 1]
    if nan(c, c1, r4, r4_1, s4, s4_1):
        return None
    if c > r4 and c1 <= r4_1:
        return "long"
    if c < s4 and c1 >= s4_1:
        return "short"
    return None
