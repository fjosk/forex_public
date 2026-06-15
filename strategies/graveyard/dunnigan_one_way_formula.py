#!/usr/bin/env python3
"""dunnigan_one_way_formula -- Outside-range full-gap bar (preliminary buy/sell) after a swing reversal. trading_systems_and_methods_kaufman_perry_j_kaufma.

Preliminary buy: today's low > prior bar's high (full outside-up bar = gap).
Confirmation: preceded by a prior swing low (fractal down).
Preliminary sell: today's high < prior bar's low (full outside-down bar).
Confirmation: preceded by a prior swing high (fractal up).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dunnigan_one_way_formula",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,close,frac_up,frac_dn",
    "long": "current low > prior bar high (full outside-up bar) AND frac_dn recently (within 5 bars)",
    "short": "current high < prior bar low (full outside-down bar) AND frac_up recently (within 5 bars)",
    "desc": "Dunnigan one-way: full-gap breakout bar after a confirmed swing reversal fractal",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch12 One-Way Formula p.292",
}


def signal(ind, pos, htf=None):
    """Dunnigan one-way: full outside-up/down bar after a recent fractal reversal."""
    if pos < 5:
        return None
    l = ind["low"][pos]
    h = ind["high"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    if nan(l, h, h1, l1):
        return None
    # Look for a recent fractal (within last 5 bars)
    recent_frac_dn = any(
        not nan(ind["frac_dn"][pos - k]) and ind["frac_dn"][pos - k] == 1
        for k in range(1, 6)
    )
    recent_frac_up = any(
        not nan(ind["frac_up"][pos - k]) and ind["frac_up"][pos - k] == 1
        for k in range(1, 6)
    )
    # Full outside-up: entire bar above prior bar (gap up)
    if l > h1 and recent_frac_dn:
        return "long"
    # Full outside-down: entire bar below prior bar (gap down)
    if h < l1 and recent_frac_up:
        return "short"
    return None
