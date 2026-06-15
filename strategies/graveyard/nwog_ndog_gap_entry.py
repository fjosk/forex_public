#!/usr/bin/env python3
"""nwog_ndog_gap_entry -- New Day/Week Opening Gap entry. ICT / Michael Huddleston.

Price gaps at the 22:00-23:00 UTC boundary (5PM-6PM EST session restart).
The gap acts as a FVG; price retraces into it and is traded back toward the
gap-open side. NWOG uses the Friday-to-Sunday gap (dow 4->6, same logic).
Note: HistData continuous M1 may show small or zero gaps; concept is worth
testing but signal frequency may be low.
Source: web:https://innercircletrader.net/tutorials/ict-new-day-opening-gap-ndog/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "nwog_ndog_gap_entry",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, open, high, low, day_open, hour_utc, atr",
    "long": "bullish gap (day_open > prev close at 22 UTC); price retraces into gap zone; close confirms rejection",
    "short": "bearish gap (day_open < prev close at 22 UTC); price retraces into gap zone; close confirms",
    "desc": "NDOG opening gap fill: trade the retrace into the session-restart gap zone",
    "source": "web:https://innercircletrader.net/tutorials/ict-new-day-opening-gap-ndog/",
}


def signal(ind, pos, htf=None):
    """NDOG: detect gap at 22-23 UTC boundary; trade retrace into gap zone during session hours."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    d_open = ind["day_open"][pos]
    h = ind["hour_utc"][pos]
    atr = ind["atr"][pos]
    h_prev = ind["hour_utc"][pos - 1]
    c_prev = ind["close"][pos - 1]
    o_cur = ind["open"][pos]
    if nan(c, lo, hi, d_open, h, atr, h_prev, c_prev, o_cur):
        return None
    if atr == 0:
        return None

    # Only look for entries during active hours (23:00-22:00 UTC = full day except boundary)
    # The gap boundary is the 22:00 bar close -> 23:00 bar open
    # We scan when the current bar is at 23:00 UTC (fresh gap bar)
    if h != 23:
        return None

    # Gap is the difference between the 22:00 close (c_prev) and the 23:00 open (o_cur)
    # We check that the previous hour was indeed 22
    if h_prev != 22:
        return None

    prior_close = c_prev
    gap_open = o_cur

    gap_size = abs(gap_open - prior_close)
    if gap_size < 0.1 * atr:
        # Gap too small (nearly zero in continuous FX feed); skip
        return None

    gap_lo = min(prior_close, gap_open)
    gap_hi = max(prior_close, gap_open)

    # Bullish gap: gap_open > prior_close; retrace back into zone = price dips into [prior_close, gap_open]
    if gap_open > prior_close:
        if lo <= gap_hi and c >= gap_lo:
            return "long"

    # Bearish gap: gap_open < prior_close; retrace up into zone = price rises into [gap_open, prior_close]
    if gap_open < prior_close:
        if hi >= gap_lo and c <= gap_hi:
            return "short"

    return None
