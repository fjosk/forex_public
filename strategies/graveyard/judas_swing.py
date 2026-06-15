#!/usr/bin/env python3
"""judas_swing -- ICT Judas Swing session-open false move and reversal. ICT / Michael Huddleston.

Price makes a false spike opposite to daily bias during the London/NY morning window
(05:00-10:00 UTC), sweeps a fractal level, then closes back through the day_open.
Entry is taken in the true direction after the return close.
Source: web:https://innercircletrader.net/tutorials/ict-judas-swing-complete-guide/
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "judas_swing",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, high, low, open, day_open, hour_utc, frac_up_px, frac_dn_px, atr, ema200",
    "long": "bearish spike below frac_dn_px during London window (05-10 UTC) then close back above day_open; ema200 bull bias",
    "short": "bullish spike above frac_up_px during London window then close back below day_open; ema200 bear bias",
    "desc": "ICT Judas Swing false open spike reversal during London killzone",
    "source": "web:https://innercircletrader.net/tutorials/ict-judas-swing-complete-guide/",
}

_KZ_START = 5   # London killzone open (UTC)
_KZ_END = 10    # London killzone close (UTC)


def signal(ind, pos, htf=None):
    """Judas Swing: false spike through fractal level during London window, body return through day_open."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    h = ind["hour_utc"][pos]
    d_open = ind["day_open"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    e200 = ind["ema200"][pos]
    if nan(c, lo, hi, h, d_open, frac_lo, frac_hi, e200):
        return None

    # Only act within the London killzone window
    if not (_KZ_START <= h < _KZ_END):
        return None

    # Coarse HTF bias via ema200
    bull_bias = c > e200
    bear_bias = c < e200

    # Long: bearish false spike below fractal low, body closes back above day_open
    if bull_bias and lo < frac_lo and c > d_open:
        return "long"

    # Short: bullish false spike above fractal high, body closes back below day_open
    if bear_bias and hi > frac_hi and c < d_open:
        return "short"

    return None
