#!/usr/bin/env python3
"""cable_swissy_false_break_fade_limit_behind_the_level -- False-break overshoot fade at S/R. currency_trading_for_dummies_2nd_edition_by_brian.

GBP/USD and USD/CHF frequently overshoot S/R by ~25-30 pips before reversing. Fade: go long when
price penetrates below Donchian low (false downside break) and CLOSES BACK above it (re-entry
confirms overshoot); go short on overshoot above Donchian high then close back below.
Uses dc_lo/dc_up as the S/R proxy.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cable_swissy_false_break_fade_limit_behind_the_level",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "low,high,close,dc_lo,dc_up",
    "long": "Low penetrates below dc_lo (false break) AND close re-enters above dc_lo -> long fade",
    "short": "High penetrates above dc_up (false break) AND close re-enters below dc_up -> short fade",
    "desc": "False-break overshoot fade: price pokes beyond S/R level then closes back inside",
    "source": "book:currency_trading_for_dummies_2nd_edition_by_brian",
}


def signal(ind, pos, htf=None):
    """False-break fade: penetrate beyond S/R then close back inside."""
    if pos < 1:
        return None
    lo   = ind["low"][pos]
    hi   = ind["high"][pos]
    c    = ind["close"][pos]
    sup  = ind["dc_lo"][pos-1]   # prior-bar S/R to avoid look-ahead
    res  = ind["dc_up"][pos-1]
    if nan(lo, hi, c, sup, res):
        return None

    # Long: current bar's low pokes below support, but closes back above it
    if lo < sup and c > sup:
        return "long"

    # Short: current bar's high pokes above resistance, but closes back below it
    if hi > res and c < res:
        return "short"

    return None
