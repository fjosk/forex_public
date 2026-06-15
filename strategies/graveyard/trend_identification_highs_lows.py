#!/usr/bin/env python3
"""trend_identification_highs_lows -- Elder: HH/HL pattern on successive swing highs/lows. elder_alexander_trading_for_a_living.

Uptrend: current fractal high > prior fractal high AND current fractal low > prior fractal low.
Downtrend: current fractal low < prior fractal low AND current fractal high < prior fractal high.
Uses frac_up_px (most recent swing high) vs prior swing high stored via frac_up_bar_high.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "trend_identification_highs_lows",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,frac_up_px,frac_dn_px",
    "long": "New fractal high > prior fractal high AND new fractal low > prior fractal low (HH+HL)",
    "short": "New fractal low < prior fractal low AND new fractal high < prior fractal high (LL+LH)",
    "desc": "Trend identification via successive HH+HL (uptrend) or LL+LH (downtrend) fractal pattern",
    "source": "elder_alexander_trading_for_a_living Sec20 p83 item1",
}


def signal(ind, pos, htf=None):
    """HH+HL structure -> long; LL+LH structure -> short."""
    if pos < 2:
        return None
    c     = ind["close"][pos]
    c1    = ind["close"][pos - 1]
    fup   = ind["frac_up_px"][pos]
    fup1  = ind["frac_up_px"][pos - 1]
    fdn   = ind["frac_dn_px"][pos]
    fdn1  = ind["frac_dn_px"][pos - 1]
    if nan(c, c1, fup, fup1, fdn, fdn1):
        return None
    # Higher high: current swing high > prior swing high
    hh = fup > fup1
    # Higher low: current swing low > prior swing low
    hl = fdn > fdn1
    # Lower low: current swing low < prior swing low
    ll = fdn < fdn1
    # Lower high: current swing high < prior swing high
    lh = fup < fup1
    if hh and hl and c > c1:
        return "long"
    if ll and lh and c < c1:
        return "short"
    return None
