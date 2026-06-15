#!/usr/bin/env python3
"""ict_macro_times -- ICT Macro Times: FVG entry inside 20-min algorithm windows.

Eight 20-minute UTC windows per day where institutional repricing is expected.
Within each window, detect a bullish or bearish FVG formed on the current bar
and enter on the retrace into that FVG (CE = 50% preferred).
Uses open_time minute-precision from epoch-ms to gate the windows.
"""
import datetime
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "ict_macro_times",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "close, high, low, open_time, frac_up_px, frac_dn_px, atr",
    "long": "Inside a macro window; sell-side liquidity swept; bullish FVG retrace",
    "short": "Inside a macro window; buy-side liquidity swept; bearish FVG retrace",
    "desc": "ICT Macro Times: FVG retrace entry within 20-min algorithm windows",
    "source": "web:https://innercircletrader.net/tutorials/ict-macro-time-based-strategy/",
}

# Macro windows: list of (start_hour_utc, start_min, end_hour_utc, end_min)
# Derived from spec EST times +5h = UTC
_MACRO_WINDOWS = [
    (7, 33, 8, 0),    # London Macro 1: 07:33-08:00 UTC
    (9, 3, 9, 30),    # London Macro 2: 09:03-09:30 UTC
    (13, 50, 14, 10), # NY AM Macro 1: 13:50-14:10 UTC
    (14, 50, 15, 10), # NY AM Macro 2: 14:50-15:10 UTC (strongest)
    (15, 50, 16, 10), # NY AM Macro 3: 15:50-16:10 UTC
    (16, 50, 17, 10), # NY Lunch Macro: 16:50-17:10 UTC
    (18, 10, 18, 40), # NY PM Macro: 18:10-18:40 UTC
    (20, 15, 20, 45), # NY Last Hour: 20:15-20:45 UTC
]


def _in_macro_window(dt):
    """Return True if dt falls inside any macro window."""
    h = dt.hour
    m = dt.minute
    t = h * 60 + m
    for (sh, sm, eh, em) in _MACRO_WINDOWS:
        s = sh * 60 + sm
        e = eh * 60 + em
        if s <= t < e:
            return True
    return False


_LOOKBACK = 20


def signal(ind, pos, htf=None):
    """ICT Macro Times FVG entry."""
    ts = ind["open_time"][pos]
    c = ind["close"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(ts, c, hi, lo):
        return None

    dt = datetime.datetime.utcfromtimestamp(ts / 1000)
    if not _in_macro_window(dt):
        return None

    # Directional bias: sweep of fractal low -> bull; sweep of fractal high -> bear
    frac_lo = ind["frac_dn_px"][pos - 1]
    frac_hi = ind["frac_up_px"][pos - 1]
    if nan(frac_lo, frac_hi):
        return None

    high = ind["high"]
    low = ind["low"]
    close = ind["close"]

    swept_low = lo < frac_lo   # sell-side liquidity swept
    swept_high = hi > frac_hi  # buy-side liquidity swept

    if swept_low:
        # Bullish bias: look for bullish FVG retrace
        for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
            if i + 1 > pos:
                continue
            g_lo = high[i - 1]; g_hi = low[i + 1]
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                continue
            mitigated = any(close[j] < g_lo for j in range(i + 1, pos) if not nan(close[j]))
            if not mitigated and lo <= g_hi and c >= g_lo:
                return "long"
            break

    if swept_high:
        # Bearish bias: look for bearish FVG retrace
        for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
            if i + 1 > pos:
                continue
            g_hi = low[i - 1]; g_lo = high[i + 1]
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                continue
            mitigated = any(close[j] > g_hi for j in range(i + 1, pos) if not nan(close[j]))
            if not mitigated and hi >= g_lo and c <= g_hi:
                return "short"
            break

    return None
