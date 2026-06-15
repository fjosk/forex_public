#!/usr/bin/env python3
"""ma_direction_turn_system_ma_exp_lrs_slope -- MA/EMA/LRS direction-change trend system; uses LRS slope and EMA slope. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ma_direction_turn_system_ma_exp_lrs_slope",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "lr_slope_price, ema20",
    "long": "Linear regression slope of price is positive AND EMA20 is rising",
    "short": "Linear regression slope of price is negative AND EMA20 is falling",
    "desc": "MA/EXP/LRS direction-turn system: LRS slope sign plus EMA slope confirmation",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch5 Table 5-2",
}


def signal(ind, pos, htf=None):
    """Long when LRS slope > 0 and EMA rising; short when LRS < 0 and EMA falling."""
    if pos < 1:
        return None
    slope = ind["lr_slope_price"][pos]
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    if nan(slope, ema, ema1):
        return None
    ema_up = ema > ema1
    ema_dn = ema < ema1
    if slope > 0 and ema_up:
        return "long"
    if slope < 0 and ema_dn:
        return "short"
    return None
