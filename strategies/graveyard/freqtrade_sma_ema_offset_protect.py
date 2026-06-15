#!/usr/bin/env python3
"""freqtrade_sma_ema_offset_protect -- EWO dip-buy: price below EMA50*0.978 with EWO confirm. thierryjmartin."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_sma_ema_offset_protect",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "ema50, ema200, rsi, close",
    "long": "close < ema50*0.978 AND (ewo>5.835 AND rsi<55) OR ewo < -19.909",
    "short": "not used (long-only per source)",
    "desc": "EWO offset protect: buy dip below EMA50 discount with Elliott Wave Oscillator confirm",
    "source": "https://github.com/thierryjmartin/freqtrade-stuff/blob/main/SMAOffsetProtectOptV1.py",
}


def signal(ind, pos, htf=None):
    """EWO dip-buy below EMA50 offset."""
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    if nan(e50, e200, r, c) or c == 0:
        return None
    ewo = (e50 - e200) / c * 100.0
    below_support = c < e50 * 0.978
    if below_support and ((ewo > 5.835 and r < 55) or ewo < -19.909):
        return "long"
    return None
