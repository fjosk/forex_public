#!/usr/bin/env python3
"""elder_ray_bull_power -- Elder Ray Bull Power TP/SL. hasnocool/tradingview-pine-scripts.

Bull Power = high - ema13. Enter long when bull_power < 0 (high still below EMA13, buyers weak).
Bear Power = low - ema13. Enter short when bear_power > 0 (low still above EMA13, sellers weak).
Uses pre-computed bear_power key; bull_power computed from high + ema13.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "elder_ray_bull_power",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "ema13, high, low, bear_power, bull_power",
    "long": "bull_power (high - ema13) < 0 AND bear_power improving (rising)",
    "short": "bear_power (low - ema13) > 0 AND bull_power declining",
    "desc": "Elder Ray: enter when high < ema13 (bull_power negative) or low > ema13 (bear_power positive)",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Elder%20Ray%20(Bull%20Power)%20TP%20and%20SL.pine",
}


def signal(ind, pos, htf=None):
    """Elder Ray: fade weak bull / bear power vs EMA13."""
    e13 = ind["ema13"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    # bear_power precomputed key = low - ema13
    bp = ind["bear_power"][pos]
    bp1 = ind["bear_power"][pos - 1]
    if nan(e13, h, lo, bp, bp1):
        return None
    bull_power = h - e13
    # Long: bull_power negative means high below ema13 -- price depressed, mean-reversion setup
    # Also confirm bear_power is rising (oversold bounce starting)
    if bull_power < 0 and bp > bp1:
        return "long"
    # Short: bear_power positive means low above ema13 -- price elevated
    # Confirm bull_power declining (overbought rollover)
    bull_power1 = ind["high"][pos - 1] - ind["ema13"][pos - 1]
    if nan(bull_power1):
        return None
    if bp > 0 and bull_power < bull_power1:
        return "short"
    return None
