#!/usr/bin/env python3
"""freqtrade_strategy004_stoch_adx_cci -- Strategy004 Stochastic ADX CCI. freqtrade.

ADX > 50 OR adx > 26 AND CCI < -100 AND stoch_k bullish cross below 20/30 thresholds = long.
Symmetric short added for FX.
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_strategy004_stoch_adx_cci",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "5m",
    "indicators": "adx, cci, stoch_k, stoch_d, ema5",
    "long": "(adx>50 OR adx>26) AND cci<-100 AND stoch_k crosses above stoch_d below oversold",
    "short": "(adx>50 OR adx>26) AND cci>100 AND stoch_k crosses below stoch_d above overbought",
    "desc": "Strategy004: ADX + CCI extreme + stochastic crossover in oversold/overbought zone",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Strategy004.py",
}


def signal(ind, pos, htf=None):
    """ADX + CCI extreme + stochastic crossover entry."""
    dx = ind["adx"][pos]
    cc = ind["cci"][pos]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(dx, cc, sk, sk1, sd, sd1):
        return None
    adx_ok = dx > 50 or dx > 26
    if adx_ok and cc < -100 and sk < 30 and sd < 30 and _xup(sk, sk1, sd, sd1):
        return "long"
    if adx_ok and cc > 100 and sk > 70 and sd > 70 and _xdn(sk, sk1, sd, sd1):
        return "short"
    return None
