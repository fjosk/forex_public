#!/usr/bin/env python3
"""bollinger_band_breakout_revert_exit -- Bollinger Band breakout entry: close penetrates upper/lower band. trading_systems_and_methods_kaufman_perry_j_kaufma.

Long: close crosses above the upper Bollinger band (breakout / reversal mode).
Short: close crosses below the lower Bollinger band.
Exit: opposite band penetration (flip) -> TREND_FLIP archetype.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "bollinger_band_breakout_revert_exit",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "close,bb_up,bb_lo,bb_mid",
    "long": "close crosses above upper Bollinger band (close > bb_up, prior close <= bb_up)",
    "short": "close crosses below lower Bollinger band",
    "desc": "Bollinger Band breakout: entry on close penetration of upper/lower band, flip on opposite",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Bands and Channels Bollinger Bands rules",
}


def signal(ind, pos, htf=None):
    """Bollinger Band breakout on close crossing the band."""
    if pos < 1:
        return None
    c   = ind["close"][pos]
    c1  = ind["close"][pos - 1]
    bbu = ind["bb_up"][pos]
    bbl = ind["bb_lo"][pos]
    if nan(c, c1, bbu, bbl):
        return None
    if c > bbu and c1 <= bbu:
        return "long"
    if c < bbl and c1 >= bbl:
        return "short"
    return None
