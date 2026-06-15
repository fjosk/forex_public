#!/usr/bin/env python3
"""fading_the_double_zeros_round_number_mean_reversion -- Fade price approaching a round-number
level when it has deviated far from SMA20. FX round-number mean reversion.

Source: day_trading_swing_trading_the_currency_market_tech, Ch.9 pp.115-120.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "fading_the_double_zeros_round_number_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "sma20, round_step, atr, close",
    "long": "Price below SMA20 by >1 ATR and close is within 0.5*ATR of nearest round level (round_step)",
    "short": "Price above SMA20 by >1 ATR and close is within 0.5*ATR of nearest round level",
    "desc": "Fade moves that overshoot SMA20 and stall near a round-number price level",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.9 pp.115-120",
}


def signal(ind, pos, htf=None):
    """Round-number fade: overextended from SMA20, price near a round-step level."""
    c = ind["close"][pos]
    s = ind["sma20"][pos]
    a = ind["atr"][pos]
    r = ind["round_step"][pos]
    if nan(c, s, a, r) or a <= 0 or r <= 0:
        return None
    dist = c - s
    # nearest round level: round c to the nearest round_step multiple
    if r > 0:
        nearest_round = round(c / r) * r
    else:
        return None
    dist_to_round = abs(c - nearest_round)
    # require price within half an ATR of the round level
    if dist_to_round > 0.5 * a:
        return None
    # long: price well below SMA20
    if dist < -1.0 * a:
        return "long"
    # short: price well above SMA20
    if dist > 1.0 * a:
        return "short"
    return None
