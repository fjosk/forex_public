#!/usr/bin/env python3
"""pivot_point_sr -- Pivot S/R level bounce with pivot bias and bullish/bearish candle confirm. web:avatrade.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_sr",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "piv_p, piv_r1, piv_r2, piv_s1, piv_s2, atr, close, open",
    "long": "close near S1 or S2 (within 0.5 ATR), bullish candle, close above pivot P",
    "short": "close near R1 or R2 (within 0.5 ATR), bearish candle, close below pivot P",
    "desc": "Pivot S/R level bounce with bias and candle-direction confirmation",
    "source": "web:https://www.avatrade.com/education/technical-analysis-indicators-strategies/pivot-points-trading-strategies",
}


def signal(ind, pos, htf=None):
    """Pivot bounce with bias + candle direction."""
    pp = ind["piv_p"][pos]
    r1, r2 = ind["piv_r1"][pos], ind["piv_r2"][pos]
    s1, s2 = ind["piv_s1"][pos], ind["piv_s2"][pos]
    atr = ind["atr"][pos]
    c, o = ind["close"][pos], ind["open"][pos]
    if nan(pp, r1, r2, s1, s2, atr, c, o):
        return None
    if atr <= 0:
        return None
    near_s = (abs(c - s1) < atr * 0.5) or (abs(c - s2) < atr * 0.5)
    near_r = (abs(c - r1) < atr * 0.5) or (abs(c - r2) < atr * 0.5)
    bull_candle = c > o
    bear_candle = c < o
    if near_s and bull_candle and c > pp:
        return "long"
    if near_r and bear_candle and c < pp:
        return "short"
    return None
