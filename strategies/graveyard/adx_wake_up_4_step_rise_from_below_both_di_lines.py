#!/usr/bin/env python3
"""adx_wake_up -- ADX rises ~4 points from below both DI lines; direction set by which DI is on top. elder_alexander_trading_for_a_living."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_wake_up_4_step_rise_from_below_both_di_lines",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "adx, di_plus, di_minus",
    "long": "ADX rises >= 4 pts from a recent low below both DI lines, and +DI > -DI",
    "short": "ADX rises >= 4 pts from a recent low below both DI lines, and -DI > +DI",
    "desc": "ADX wake-up: 4-step rise from below both DI lines signals new trend birth; direction = which DI is on top",
    "source": "elder_alexander_trading_for_a_living",
}


def signal(ind, pos, htf=None):
    """ADX 4-point rise from a trough below both DI lines."""
    if pos < 5:
        return None
    adx = ind["adx"]
    dip = ind["di_plus"]
    dim = ind["di_minus"]
    a = adx[pos]
    dp = dip[pos]
    dm = dim[pos]
    if nan(a, dp, dm):
        return None

    # find recent minimum ADX over the last 5 bars
    adx_min = a
    for k in range(1, 6):
        if pos - k < 0:
            break
        av = adx[pos - k]
        if nan(av):
            continue
        if av < adx_min:
            adx_min = av

    # ADX must have risen >= 4 points from its recent trough
    if a - adx_min < 4.0:
        return None

    # At the trough, ADX was below both DI lines
    # Approximate: current ADX only recently crossed up; check trough was below both DIs
    # Use current DI values as proxy (sufficient for a systematic rule)
    trough_below_both = adx_min < dp and adx_min < dm
    if not trough_below_both:
        return None

    if dp > dm:
        return "long"
    if dm > dp:
        return "short"
    return None
