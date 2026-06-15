#!/usr/bin/env python3
"""breakout_above_prior_range_resistance -- Close breaks above long-established Donchian upper after a range period. the_naked_trader."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "breakout_above_prior_range_resistance",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, close, bb_width",
    "long": "close breaks above Donchian upper after a low-bbwidth (tight range) compression period",
    "short": "no short side (Naked Trader describes long-only breakout)",
    "desc": "Breakout above prior range resistance: close above Donchian upper after Bollinger compression confirms long-established range",
    "source": "the_naked_trader_how_anyone_can_still_make_money_t",
}


def signal(ind, pos, htf=None):
    """Close above Donchian upper after volatility compression (bbw_pct low = prolonged range)."""
    if pos < 3:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    bwp = ind["bbw_pct"][pos - 1]
    if nan(c, dc_up, bwp):
        return None
    # Require prior range compression (bbw_pct in lower third = below 33rd percentile proxy)
    # Use absolute threshold: bbw_pct < 0.33 means band narrower than its historical norm
    if bwp > 0.33:
        return None
    if c > dc_up:
        return "long"
    return None
