#!/usr/bin/env python3
"""dual_thrust_opening_range -- Dual Thrust opening range breakout (je-suis-tm). web:github.com/je-suis-tm."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "dual_thrust_opening_range",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "day_open, hh_n, ll_n, close, hour_utc",
    "long": "close > day_open + 0.5 * (hh_n - ll_n) and hour_utc < 17",
    "short": "close < day_open - 0.5 * (hh_n - ll_n) and hour_utc < 17",
    "desc": "Dual Thrust opening range breakout with session close (je-suis-tm / Michael Chalek)",
    "source": "web:https://github.com/je-suis-tm/quant-trading",
}

_PARAM = 0.5
_SESSION_CLOSE_UTC = 17


def signal(ind, pos, htf=None):
    """Dual Thrust: adaptive range from hh_n/ll_n around day_open; close before 17 UTC."""
    cl = ind["close"][pos]
    hr = ind["hour_utc"][pos]
    dopen = ind["day_open"][pos]
    hhn = ind["hh_n"][pos]
    lln = ind["ll_n"][pos]
    if nan(cl, hr, dopen, hhn, lln):
        return None
    if hr >= _SESSION_CLOSE_UTC:
        return None
    rng = hhn - lln
    if rng <= 0:
        return None
    upper = dopen + _PARAM * rng
    lower = dopen - _PARAM * rng
    if cl > upper:
        return "long"
    if cl < lower:
        return "short"
    return None
