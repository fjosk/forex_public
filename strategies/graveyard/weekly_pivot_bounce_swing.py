#!/usr/bin/env python3
"""weekly_pivot_bounce_swing -- Weekly pivot point bounce with reversal candle confirmation. web:admiralmarkets.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "weekly_pivot_bounce_swing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "piv_p, piv_r1, piv_s1, atr, close, open, low, high",
    "long": "above weekly pivot, price near piv_p or piv_s1, bullish candle reversal",
    "short": "below weekly pivot, price near piv_p or piv_r1, bearish candle reversal",
    "desc": "Weekly pivot bounce swing -- price at pivot level with reversal candle",
    "source": "web:https://admiralmarkets.com/education/articles/forex-indicators/pivot-point-trading-identifying-support-and-resistance-levels-with-a-pivot-point-indicator",
}


def signal(ind, pos, htf=None):
    """Weekly pivot bounce: near pivot/S1/R1 with reversal candle and bias."""
    pp = ind["piv_p"][pos]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    atr = ind["atr"][pos]
    c, o = ind["close"][pos], ind["open"][pos]
    lo1 = ind["low"][pos - 1]
    hi1 = ind["high"][pos - 1]
    if nan(pp, r1, s1, atr, c, o, lo1, hi1):
        return None
    if atr <= 0:
        return None
    # Long: above pivot bias, prior bar touched pp or s1 zone, bullish reversal
    at_pp_or_s1 = (lo1 <= pp + atr * 0.5) or (lo1 <= s1 + atr * 0.5)
    if c > pp and at_pp_or_s1 and c > o:
        return "long"
    # Short: below pivot bias, prior bar touched pp or r1 zone, bearish reversal
    at_pp_or_r1 = (hi1 >= pp - atr * 0.5) or (hi1 >= r1 - atr * 0.5)
    if c < pp and at_pp_or_r1 and c < o:
        return "short"
    return None
