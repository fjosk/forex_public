#!/usr/bin/env python3
"""five_ema_ten_ema_stoch_rsi_system -- EMA5/EMA8 cross + Stoch trend + RSI>50 filter. QuantConnect Easy System."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "five_ema_ten_ema_stoch_rsi_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1d",
    "indicators": "ema5, ema8, stoch_k, stoch_d, rsi",
    "long": "EMA5 crosses above EMA8 AND stoch_k+stoch_d trending up AND stoch_k < 80 AND RSI > 50",
    "short": "EMA5 crosses below EMA8 AND stoch_k+stoch_d trending down AND stoch_k > 20 AND RSI < 50",
    "desc": "5/10 EMA cross + Stochastic trend direction + RSI momentum filter (So Easy It's Ridiculous system)",
    "source": "QuantConnect forum discussion/6585 community post; no backtest stats",
}


def signal(ind, pos, htf=None):
    """EMA5/8 cross with Stochastic trend and RSI momentum confirmation."""
    e5 = ind["ema5"][pos]
    e5_1 = ind["ema5"][pos - 1]
    e8 = ind["ema8"][pos]
    e8_1 = ind["ema8"][pos - 1]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    r = ind["rsi"][pos]
    if nan(e5, e5_1, e8, e8_1, sk, sk1, sd, sd1, r):
        return None
    cross_up = _xup(e5, e5_1, e8, e8_1)
    cross_dn = _xdn(e5, e5_1, e8, e8_1)
    stoch_up = sk > sk1 and sd > sd1
    stoch_dn = sk < sk1 and sd < sd1
    if cross_up and stoch_up and sk < 80 and r > 50:
        return "long"
    if cross_dn and stoch_dn and sk > 20 and r < 50:
        return "short"
    return None
