#!/usr/bin/env python3
"""swing_point_ringed_high_low -- Break of most recent fractal swing high/low signals trend change. long_term_secrets_to_short_term_trading.

Long: price exceeds the most recent fractal high (frac_up_px) -> trend reversal up.
Short: price falls below the most recent fractal low (frac_dn_px) -> trend reversal down.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "swing_point_ringed_high_low_trend_change",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,high,low,frac_up_px,frac_dn_px",
    "long": "price (high) breaks above most recent fractal swing high -> trend reversal up",
    "short": "price (low) breaks below most recent fractal swing low -> trend reversal down",
    "desc": "Swing-point ringed high/low: fractal breakout signals trend change direction",
    "source": "long_term_secrets_to_short_term_trading Ch9 Figures 9.1-9.4 pp133-136",
}


def signal(ind, pos, htf=None):
    """Break of fractal swing extreme signals trend reversal."""
    if pos < 1:
        return None
    hi    = ind["high"][pos]
    lo    = ind["low"][pos]
    hi1   = ind["high"][pos - 1]
    lo1   = ind["low"][pos - 1]
    fup   = ind["frac_up_px"][pos]
    fdn   = ind["frac_dn_px"][pos]
    if nan(hi, lo, hi1, lo1, fup, fdn):
        return None
    # Long: high breaks above the most recent fractal high (prior bar did not)
    if hi > fup and hi1 <= fup:
        return "long"
    # Short: low breaks below the most recent fractal low (prior bar did not)
    if lo < fdn and lo1 >= fdn:
        return "short"
    return None
