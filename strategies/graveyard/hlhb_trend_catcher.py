#!/usr/bin/env python3
"""hlhb_trend_catcher -- HLHB: EMA5/EMA20 cross + RSI 50 cross + ADX>25 filter. BabyPips/Huck."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "hlhb_trend_catcher",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema20, rsi, adx",
    "long": "EMA5 crosses above EMA20 AND rsi crosses above 50 AND adx > 25",
    "short": "EMA5 crosses below EMA20 AND rsi crosses below 50 AND adx > 25",
    "desc": "HLHB Trend-Catcher: dual EMA cross + RSI 50 cross with ADX trend filter",
    "source": "web:https://www.babypips.com/trading/forex-hlhb-system-explained",
}


def signal(ind, pos, htf=None):
    """EMA5/EMA20 crossover AND RSI 50 crossover, both on same bar, ADX filter."""
    e5 = ind["ema5"][pos]
    e5p = ind["ema5"][pos - 1]
    e20 = ind["ema20"][pos]
    e20p = ind["ema20"][pos - 1]
    rs = ind["rsi"][pos]
    rsp = ind["rsi"][pos - 1]
    adx = ind["adx"][pos]
    if nan(e5, e5p, e20, e20p, rs, rsp, adx):
        return None
    ema_long = _xup(e5, e5p, e20, e20p)
    ema_short = _xdn(e5, e5p, e20, e20p)
    rsi_up = rs > 50 and rsp <= 50
    rsi_dn = rs < 50 and rsp >= 50
    adx_ok = adx > 25
    if ema_long and rsi_up and adx_ok:
        return "long"
    if ema_short and rsi_dn and adx_ok:
        return "short"
    return None
