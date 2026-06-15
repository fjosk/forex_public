#!/usr/bin/env python3
"""intraday_breakout_prev_day_hl -- Screen-3 breakout entry: buy stop at prior day high, sell stop at prior day low. come_into_my_trading_room_elder."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "intraday_breakout_bottom_fishing_entry_screen_three_techniques",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "prev_dhh, prev_dll, high, low",
    "long": "high trades above prior day high (buy stop breakout entry)",
    "short": "low trades below prior day low (sell stop breakout entry)",
    "desc": "Triple Screen Screen-3 breakout entry: buy stop at previous day high / sell stop at previous day low",
    "source": "come_into_my_trading_room_alexander_elder",
}


def signal(ind, pos, htf=None):
    """Break above prior day high = long; break below prior day low = short."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    ph = ind["prev_dhh"][pos]
    pl = ind["prev_dll"][pos]
    if nan(h, l, ph, pl):
        return None
    if h > ph:
        return "long"
    if l < pl:
        return "short"
    return None
