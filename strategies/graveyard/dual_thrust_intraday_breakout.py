#!/usr/bin/env python3
"""dual_thrust_intraday_breakout -- Dual Thrust dynamic range breakout (QuantConnect). web:quantconnect.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "dual_thrust_intraday_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "day_open, hh_n, ll_n, prev_dhc, prev_dlc, close, hour_utc",
    "long": "close > day_open + 0.5 * range (Dual Thrust cap)",
    "short": "close < day_open - 0.5 * range (Dual Thrust floor)",
    "desc": "Dual Thrust intraday breakout: dynamic range from N-day OHLC extremes (Chalek/QuantConnect)",
    "source": "web:https://www.quantconnect.com/learning/articles/investment-strategy-library/dual-thrust-trading-algorithm",
}

_K1 = 0.5
_K2 = 0.5


def signal(ind, pos, htf=None):
    """Dual Thrust: close vs adaptive cap/floor around day_open."""
    cl = ind["close"][pos]
    dopen = ind["day_open"][pos]
    hhn = ind["hh_n"][pos]
    lln = ind["ll_n"][pos]
    # Use prev_dhc/prev_dlc as close extremes (previous day high-close, low-close)
    dhc = ind["prev_dhc"][pos]
    dlc = ind["prev_dlc"][pos]
    if nan(cl, dopen, hhn, lln, dhc, dlc):
        return None
    # range = max(HH - lowest_close, highest_close - LL)
    rng = max(hhn - dlc, dhc - lln)
    if rng <= 0:
        return None
    cap = dopen + _K1 * rng
    floor_ = dopen - _K2 * rng
    if cl > cap:
        return "long"
    if cl < floor_:
        return "short"
    return None
