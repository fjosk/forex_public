#!/usr/bin/env python3
"""range_bound_rsi_stoch_bounce -- Range RSI+Stochastic bounce at pivot S/R. PaxForex."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "range_bound_rsi_stoch_bounce",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h/4h",
    "indicators": "adx, rsi, stoch_k, stoch_d, piv_s1, piv_r1, body_mom",
    "long": "ADX<25, near piv_s1, RSI<30, stoch_k crosses above stoch_d from oversold, bullish candle",
    "short": "ADX<25, near piv_r1, RSI>70, stoch_k crosses below stoch_d from overbought, bearish candle",
    "desc": "Range-bound RSI + Stochastic bounce at pivot support/resistance",
    "source": "web:https://paxforex.org/forex-blog/forex-range-trading-strategies",
}


def signal(ind, pos, htf=None):
    """Ranging market bounce: ADX gate + RSI extreme + Stoch cross at pivot."""
    if pos < 1:
        return None
    adx = ind["adx"][pos]
    rsi = ind["rsi"][pos]
    sk0 = ind["stoch_k"][pos]
    sd0 = ind["stoch_d"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd1 = ind["stoch_d"][pos - 1]
    c = ind["close"][pos]
    ps1 = ind["piv_s1"][pos]
    pr1 = ind["piv_r1"][pos]
    bm = ind["body_mom"][pos]
    if nan(adx, rsi, sk0, sd0, sk1, sd1, c, ps1, pr1, bm):
        return None

    ranging = adx < 25

    near_support = c <= ps1 * 1.002
    stoch_xup = sk0 > sd0 and sk1 <= sd1 and sk0 < 20
    if ranging and near_support and rsi < 30 and stoch_xup and bm > 0:
        return "long"

    near_resistance = c >= pr1 * 0.998
    stoch_xdn = sk0 < sd0 and sk1 >= sd1 and sk0 > 80
    if ranging and near_resistance and rsi > 70 and stoch_xdn and bm < 0:
        return "short"

    return None
