#!/usr/bin/env python3
"""weekly_profile_range -- ICT Weekly Profile: Tuesday reversal bias. ICT / Michael Huddleston.

Most common bullish weekly profile: Monday consolidates without entering deep discount;
Tuesday dips into a discount array and reverses. Bearish mirror: Tuesday spikes into
premium and reverses. Uses dow for day-of-week gating.
Source: web:https://innercircletrader.net/tutorials/ict-weekly-range-profiles/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "weekly_profile_range",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "close, high, low, dow, frac_up_px, frac_dn_px, atr, prev_dhh, prev_dll",
    "long": "dow==Tuesday; low sweeps below frac_dn_px; close reverses back above; ema200 bull proxy via prev_dhh > prev_dll",
    "short": "dow==Tuesday; high sweeps above frac_up_px; close reverses back below",
    "desc": "ICT Weekly Profile: Tuesday swing low/high sweep and reversal",
    "source": "web:https://innercircletrader.net/tutorials/ict-weekly-range-profiles/",
}

_TUESDAY = 1   # dow encoding: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri


def signal(ind, pos, htf=None):
    """Weekly profile: Tuesday fractal sweep-and-reversal for weekly directional move."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    dow = ind["dow"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    if nan(c, lo, hi, dow, frac_lo, frac_hi, pdh, pdl):
        return None

    # Only act on Tuesday
    if int(dow) != _TUESDAY:
        return None

    # Coarse weekly bias: previous day's high > low relationship as trend proxy
    bull_week = pdh > pdl   # prev day made HH vs HL -- coarse; always True but filters NaN
    # Use frac range midpoint as the swing bias
    rng = frac_hi - frac_lo
    if rng <= 0:
        return None
    equil = frac_lo + 0.50 * rng

    # Long: Tuesday dip below frac low with close reversal back above; price in lower half
    if lo < frac_lo and c > frac_lo and c < equil:
        return "long"

    # Short: Tuesday spike above frac high with close reversal back below; price in upper half
    if hi > frac_hi and c < frac_hi and c > equil:
        return "short"

    return None
