#!/usr/bin/env python3
"""breakout_channel_risk_definition_n_period -- N-period Donchian high/low channel breakout; risk = channel width. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "breakout_channel_risk_definition_n_period_high_low_entry",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close equals highest-close for the period (new N-period Donchian high)",
    "short": "close equals lowest-close for the period (new N-period Donchian low); reverse on opposite",
    "desc": "Breakout-channel risk definition: Donchian N-period close breakout, always-in with channel-width risk",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Donchian close breakout with stop-and-reverse on opposite extreme."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_up, dc_lo):
        return None
    if c >= dc_up:
        return "long"
    if c <= dc_lo:
        return "short"
    return None
