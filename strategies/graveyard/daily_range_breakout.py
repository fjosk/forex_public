#!/usr/bin/env python3
"""daily_range_breakout -- Asian session (00:00-06:00 UTC) high/low breakout in London window. web:mql5.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "daily_range_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "close > Asian session (00-06 UTC) high, current hour 06-10 UTC",
    "short": "close < Asian session (00-06 UTC) low, current hour 06-10 UTC",
    "desc": "Daily range breakout: Asian session high/low, trade during London window 06-10 UTC",
    "source": "web:https://www.mql5.com/en/articles/16135",
}

_SESSION_START = 0   # UTC hour
_SESSION_END = 6     # UTC hour (exclusive)
_VALID_START = 6     # trade window start
_VALID_END = 10      # trade window end (exclusive)
_LOOKBACK = 20       # bars to scan back for the session window


def signal(ind, pos, htf=None):
    """Asian session high/low breakout; trade only in London window (06-10 UTC)."""
    hr = ind["hour_utc"][pos]
    cl = ind["close"][pos]
    if nan(hr, cl):
        return None
    if not (_VALID_START <= hr < _VALID_END):
        return None
    # scan back to find Asian session high and low
    session_hi = None
    session_lo = None
    for i in range(1, min(_LOOKBACK, pos) + 1):
        h_bar = ind["hour_utc"][pos - i]
        hi_bar = ind["high"][pos - i]
        lo_bar = ind["low"][pos - i]
        if nan(h_bar, hi_bar, lo_bar):
            continue
        if _SESSION_START <= h_bar < _SESSION_END:
            if session_hi is None or hi_bar > session_hi:
                session_hi = hi_bar
            if session_lo is None or lo_bar < session_lo:
                session_lo = lo_bar
    if session_hi is None or session_lo is None:
        return None
    if cl > session_hi:
        return "long"
    if cl < session_lo:
        return "short"
    return None
