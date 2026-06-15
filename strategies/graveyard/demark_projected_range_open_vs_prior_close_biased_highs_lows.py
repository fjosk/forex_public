#!/usr/bin/env python3
"""demark_projected_range_open_vs_prior_close_biased_highs_lows -- DeMark projected high/low: buy near projected low, sell near projected high. trading_systems_and_methods_kaufman_perry_j_kaufma Ch15."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "demark_projected_range_open_vs_prior_close_biased_highs_lows",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "open,high,low,close (DeMark projection computed inline from prior OHLC)",
    "long": "Price trades down to DeMark projected low (support), entry on next bar",
    "short": "Price trades up to DeMark projected high (resistance), entry on next bar",
    "desc": "DeMark projected range: bias-adjusted daily H/L projections used as intrabar S/R for entry",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch15",
}


def _demark_levels(o, h, l, c):
    """Compute DeMark projected high and low from prior-day OHLC."""
    if c < o:
        x = (h + c + 2.0 * l) / 2.0
    elif c > o:
        x = (2.0 * h + l + c) / 2.0
    else:
        x = (h + l + 2.0 * c) / 2.0
    proj_high = x - l
    proj_low = x - h
    return proj_high, proj_low


def signal(ind, pos, htf=None):
    """Long when price touches DeMark projected low; short when it touches projected high."""
    if pos < 1:
        return None
    # Current bar
    c_now = ind["close"][pos]
    l_now = ind["low"][pos]
    h_now = ind["high"][pos]
    # Prior bar OHLC for projection
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(c_now, l_now, h_now, o1, h1, l1, c1):
        return None
    proj_high, proj_low = _demark_levels(o1, h1, l1, c1)
    if nan(proj_high, proj_low):
        return None
    # Long: current bar's low touches or goes below projected low (support test)
    if l_now <= proj_low and c_now > proj_low:
        return "long"
    # Short: current bar's high touches or exceeds projected high (resistance test)
    if h_now >= proj_high and c_now < proj_high:
        return "short"
    return None
