#!/usr/bin/env python3
"""trend_direction_swing_structure -- Elder/Dow: HH/HL structure via fractal break confirms trend. elder_alexander_trading_for_a_living.

Long: price (close) breaks above the last fractal swing high -> uptrend confirmed, enter long.
Short: price breaks below the last fractal swing low -> downtrend confirmed, enter short.
Maps the Dow theory / trendline break rule using the engine's fractal swing extremes.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "trend_direction_via_swing_structure_trendline_break",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,frac_up_px,frac_dn_px",
    "long": "close breaks above the most recent fractal swing high -> HH structure, uptrend long",
    "short": "close breaks below the most recent fractal swing low -> LL structure, downtrend short",
    "desc": "Swing-structure trend: fractal HH break confirms uptrend; fractal LL break confirms downtrend",
    "source": "elder_alexander_trading_for_a_living Sec20 Figure 20-1",
}


def signal(ind, pos, htf=None):
    """Fractal swing break confirms trend direction."""
    if pos < 1:
        return None
    c   = ind["close"][pos]
    c1  = ind["close"][pos - 1]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    if nan(c, c1, fup, fdn):
        return None
    if c > fup and c1 <= fup:
        return "long"
    if c < fdn and c1 >= fdn:
        return "short"
    return None
