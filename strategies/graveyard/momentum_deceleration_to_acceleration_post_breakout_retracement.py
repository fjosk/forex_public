#!/usr/bin/env python3
"""momentum_deceleration_to_acceleration_post_breakout_retracement -- After a Donchian breakout,
detect deceleration then re-acceleration using the Accelerator Oscillator (ac): re-enter when ac
flips positive (after a brief negative dip) following an upside breakout.

Source: trade_your_way_to_financial_freedom_mabroke_blogsp, Ch.8.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "momentum_deceleration_to_acceleration_post_breakout_retracement",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, ac, close",
    "long": "Close > dc_up[N] (recent upside breakout) AND ac dipped then re-turned positive (ac > 0 > ac[1])",
    "short": "Close < dc_lo[N] (recent downside breakout) AND ac dipped then re-turned negative (ac < 0 < ac[1])",
    "desc": "Post-breakout deceleration-to-acceleration re-entry: Donchian breakout + AC oscillator pullback/re-acceleration",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.8",
}

_LOOK = 10  # bars to look back for the breakout


def signal(ind, pos, htf=None):
    """Donchian breakout + AC re-acceleration after pullback."""
    if pos < _LOOK + 1:
        return None
    c = ind["close"][pos]
    ac = ind["ac"][pos]
    ac1 = ind["ac"][pos - 1]
    if nan(c, ac, ac1):
        return None
    # Check for a recent upside breakout
    recent_breakout_up = False
    recent_breakout_dn = False
    for k in range(1, _LOOK + 1):
        dup = ind["dc_up"][pos - k]
        dlo = ind["dc_lo"][pos - k]
        ck = ind["close"][pos - k]
        if nan(dup, dlo, ck):
            continue
        if ck > dup:
            recent_breakout_up = True
        if ck < dlo:
            recent_breakout_dn = True

    # Long: recent breakout up + AC just turned from negative to positive (decel->accel)
    if recent_breakout_up and ac > 0 and ac1 <= 0:
        return "long"
    # Short: recent breakout down + AC just turned from positive to negative
    if recent_breakout_dn and ac < 0 and ac1 >= 0:
        return "short"
    return None
