#!/usr/bin/env python3
"""macd_15m_swing_scalp -- MACD histogram cross with EMA50 trend filter. web:forextraders.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_15m_swing_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "15m",
    "indicators": "macd_hist, ema50",
    "long": "macd_hist turns positive (cross up) AND close > ema50",
    "short": "macd_hist turns negative (cross down) AND close < ema50",
    "desc": "MACD histogram sign-change with EMA50 trend filter 15m scalp",
    "source": "web:https://forextraders.com/forex-education/forex-scalping/simple-1-5-and-15-minute-forex-scalping-strategies/",
}


def signal(ind, pos, htf=None):
    """MACD histogram just turned positive/negative while price is on the trend side of EMA50."""
    mh = ind["macd_hist"][pos]
    mh_p = ind["macd_hist"][pos - 1]
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    if nan(mh, mh_p, e50, c):
        return None
    macd_cross_up = mh > 0 and mh_p <= 0
    macd_cross_dn = mh < 0 and mh_p >= 0
    if macd_cross_up and c > e50:
        return "long"
    if macd_cross_dn and c < e50:
        return "short"
    return None
