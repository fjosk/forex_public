#!/usr/bin/env python3
"""yearly_position_breakout_context -- 12-month range thirds context filter for breakout. encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul.

Classify current close within prior 12-month range thirds; combine with Donchian breakout direction.
Favor longs when price is in the low third breaking upward; favor shorts when in the high third breaking downward.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "yearly_position_breakout_context",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "yr_high,yr_low,dc_up,dc_lo,close",
    "long": "close > dc_up (Donchian breakout up) AND close in lower third of 12-month range",
    "short": "close < dc_lo (Donchian breakout down) AND close in upper third of 12-month range",
    "desc": "Yearly range thirds context: combine Donchian breakout with 12-month range position for directional bias",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul, p.992 + p.983",
}


def signal(ind, pos, htf=None):
    """Donchian breakout filtered by 12-month range thirds position."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    yr_hi = ind["yr_high"][pos]
    yr_lo = ind["yr_low"][pos]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c, yr_hi, yr_lo, dc_up, dc_lo, c1):
        return None
    yr_rng = yr_hi - yr_lo
    if yr_rng <= 0:
        return None
    third = yr_rng / 3.0
    # Thirds: low_third = yr_lo to yr_lo+third; high_third = yr_hi-third to yr_hi
    in_low_third = c <= yr_lo + third
    in_high_third = c >= yr_hi - third
    broke_up = c > dc_up and c1 <= dc_up
    broke_dn = c < dc_lo and c1 >= dc_lo
    if broke_up and in_low_third:
        return "long"
    if broke_dn and in_high_third:
        return "short"
    return None
