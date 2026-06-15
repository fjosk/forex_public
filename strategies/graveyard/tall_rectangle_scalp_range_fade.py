#!/usr/bin/env python3
"""tall_rectangle_scalp_range_fade -- Inside a confirmed rectangle range, go long near the bottom
trendline when price turns up; short near the top trendline when price turns down.

Source: encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul, Ch.37 Table 37.9.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "tall_rectangle_scalp_range_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, dc_lo, dc_up, chop",
    "long": "Range confirmed (chop > 50); low <= dc_lo and close > close[1] (direction change up from bottom)",
    "short": "Range confirmed (chop > 50); high >= dc_up and close < close[1] (direction change down from top)",
    "desc": "Tall rectangle intra-range scalp: buy bottom trendline on reversal, sell top trendline on reversal",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul Ch.37 Table 37.9",
}

_CHOP_THRESH = 50.0
_TOL_FRAC = 0.05  # within 5% of band edge


def signal(ind, pos, htf=None):
    """Rectangle scalp: touch band edge + reversal close direction."""
    if pos < 1:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    ch = ind["chop"][pos]
    if nan(c0, c1, lo, hi, dlo, dup, ch) or dup <= dlo:
        return None
    if ch <= _CHOP_THRESH:
        return None
    tol = _TOL_FRAC * (dup - dlo)
    if lo <= dlo + tol and c0 > c1:
        return "long"
    if hi >= dup - tol and c0 < c1:
        return "short"
    return None
