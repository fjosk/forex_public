#!/usr/bin/env python3
"""opening_range_breakout_psar_trail -- ORB with ADX/DI trend filter and PSAR trail. QuantConnect."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "opening_range_breakout_psar_trail",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "adx, di_plus, di_minus, psar_dir, high, low, close, hour_utc",
    "long": "close > session opening range high AND adx>20 AND di_plus>di_minus AND hour_utc<12",
    "short": "close < session opening range low AND adx>20 AND di_minus>di_plus AND hour_utc<12",
    "desc": "Opening range breakout with ADX/DI trend filter; PSAR trail via exit preset",
    "source": "web:https://www.quantconnect.com/forum/discussion/799/strategy-opening-range-breakout/",
}

_OPEN_HOUR = 8
_CUTOFF_HOUR = 12
_ADX_MIN = 20


def signal(ind, pos, htf=None):
    """Breakout above/below early-session range, gated by ADX trend strength and time."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    adx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    if nan(hour, c, adx, dip, dim):
        return None
    ih = int(hour)
    if ih < _OPEN_HOUR or ih >= _CUTOFF_HOUR:
        return None
    if adx < _ADX_MIN:
        return None
    # Compute range from the first two bars of the session (hour 8-9 UTC)
    hi = lo = None
    for i in range(pos - 1, max(pos - 6, 0), -1):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            break
        if int(h_i) < _OPEN_HOUR:
            break
        bar_hi = ind["high"][i]
        bar_lo = ind["low"][i]
        if nan(bar_hi, bar_lo):
            continue
        hi = bar_hi if hi is None else max(hi, bar_hi)
        lo = bar_lo if lo is None else min(lo, bar_lo)
    if hi is None or lo is None:
        return None
    if c > hi and dip > dim:
        return "long"
    if c < lo and dim > dip:
        return "short"
    return None
