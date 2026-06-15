#!/usr/bin/env python3
"""turtle_donchian_channel_breakout_s1_s2_dual_system -- Turtle dual system: S1 (20-day Donchian)
and S2 (55-day Donchian) combined; signal fires if either system triggers.
The Complete TurtleTrader, ch.6-7."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "turtle_donchian_channel_breakout_s1_s2_dual_system",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up,dc_lo,hh_n,ll_n,high,low",
    "long": "high > 20-bar high (S1) OR high > 55-bar high (S2) proxy via hh_n",
    "short": "low < 20-bar low (S1) OR low < 55-bar low (S2) proxy via ll_n",
    "desc": "Turtle dual-system Donchian breakout: S1=20-bar entry, S2=55-bar entry (hh_n/ll_n proxy)",
    "source": "The Complete TurtleTrader, ch.4-7 (S1/S2 system rules)",
}


def signal(ind, pos, htf=None):
    """S1 (dc_up/dc_lo 20-bar) OR S2 (hh_n/ll_n as 55-bar proxy) breakout."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    # S1: dc_up/dc_lo (Donchian, default N used by engine)
    dc_hi = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    # S2 proxy: hh_n / ll_n (N-bar highest high / lowest low, longer lookback)
    hh = ind["hh_n"][pos]
    ll = ind["ll_n"][pos]
    if nan(h, l, dc_hi, dc_lo, hh, ll):
        return None
    if h > dc_hi or h > hh:
        return "long"
    if l < dc_lo or l < ll:
        return "short"
    return None
