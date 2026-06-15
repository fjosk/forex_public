#!/usr/bin/env python3
"""dual_thrust -- Dual Thrust breakout using prev-day OHLC range (je-suis-tm/Chalek). web:github.com/je-suis-tm."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "dual_thrust",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "day_open, prev_dhh, prev_dll, prev_dhc, prev_dlc, close, hour_utc",
    "long": "close > day_open + 0.5 * range; range = max(prev_dhh-prev_dlc, prev_dhc-prev_dll)",
    "short": "close < day_open - 0.5 * range",
    "desc": "Dual Thrust (Chalek): prior-day OHLC range triggers, flatten at 12:00 EST (17 UTC)",
    "source": "web:https://github.com/je-suis-tm/quant-trading",
}

_PARAM = 0.5
_FLATTEN_UTC = 17


def signal(ind, pos, htf=None):
    """Dual Thrust using prev-day OHLC: cap = day_open + K * range."""
    cl = ind["close"][pos]
    hr = ind["hour_utc"][pos]
    dopen = ind["day_open"][pos]
    dhh = ind["prev_dhh"][pos]
    dll = ind["prev_dll"][pos]
    dhc = ind["prev_dhc"][pos]
    dlc = ind["prev_dlc"][pos]
    if nan(cl, hr, dopen, dhh, dll, dhc, dlc):
        return None
    if hr >= _FLATTEN_UTC:
        return None
    rng = max(dhh - dlc, dhc - dll)
    if rng <= 0:
        return None
    cap = dopen + _PARAM * rng
    floor_ = dopen - _PARAM * rng
    if cl > cap:
        return "long"
    if cl < floor_:
        return "short"
    return None
