#!/usr/bin/env python3
"""nested_multi_timeframe_swing_trend_st_it_lt_pivots -- Nested swing structure: short-term low higher than prior short-term low = IT uptrend; enter on structure confirmation. Williams.

tier1 multi-timeframe. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "nested_multi_timeframe_swing_trend_st_it_lt_pivots",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "frac_up_px, frac_dn_px, frac_up, frac_dn, close",
    "long": "New fractal low is HIGHER than prior fractal low (higher-low structure = uptrend)",
    "short": "New fractal high is LOWER than prior fractal high (lower-high structure = downtrend)",
    "desc": "Nested swing trend: higher fractal lows confirm uptrend; lower fractal highs confirm downtrend",
    "source": "Williams, Long-Term Secrets to Short-Term Trading, Ch.1 Defining Intermediate Highs/Lows, pp.17-22",
}


def signal(ind, pos, htf=None):
    """Higher fractal low = long; lower fractal high = short."""
    if pos < 2:
        return None
    fup = ind["frac_up"][pos]
    fdn = ind["frac_dn"][pos]
    fup1 = ind["frac_up"][pos - 1]
    fdn1 = ind["frac_dn"][pos - 1]
    fup_px = ind["frac_up_px"][pos]
    fdn_px = ind["frac_dn_px"][pos]
    fup_px1 = ind["frac_up_px"][pos - 1]
    fdn_px1 = ind["frac_dn_px"][pos - 1]
    c = ind["close"][pos]
    if nan(c):
        return None
    # Long: current fractal low is higher than prior fractal low
    if not nan(fdn, fdn1, fdn_px, fdn_px1):
        if fdn and fdn1 and fdn_px > fdn_px1:
            return "long"
    # Short: current fractal high is lower than prior fractal high
    if not nan(fup, fup1, fup_px, fup_px1):
        if fup and fup1 and fup_px < fup_px1:
            return "short"
    return None
