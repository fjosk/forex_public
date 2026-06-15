#!/usr/bin/env python3
"""stochastic_rsi_macd_triple_confirm -- Stochastic + RSI + MACD Triple Confirmation Strategy.
web:https://medium.com/@boyangchen02/backtesting-a-stochastic-rsi-macd-cryptocurrency-trading-strategy-using-python-9f880abf52e6
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "stochastic_rsi_macd_triple_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "30m",
    "indicators": "stoch_k, stoch_d, rsi, macd, macd_sig",
    "long": "stoch_k>75 and stoch_d>75 AND rsi>50 AND MACD crosses above signal",
    "short": "stoch_k<25 and stoch_d<25 AND rsi<50 AND MACD crosses below signal",
    "desc": "Three-indicator majority-confirm: all of stochastic/RSI/MACD must agree on direction",
    "source": "web:https://medium.com/@boyangchen02/backtesting-a-stochastic-rsi-macd-cryptocurrency-trading-strategy-using-python-9f880abf52e6",
}


def signal(ind, pos, htf=None):
    """Triple confirmation: stochastic momentum zone + RSI midline + MACD cross all agree."""
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    rs = ind["rsi"][pos]
    mc = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    mc1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(sk, sd, rs, mc, ms, mc1, ms1):
        return None
    macd_xup = mc > ms and mc1 <= ms1
    macd_xdn = mc < ms and mc1 >= ms1
    if sk > 75 and sd > 75 and rs > 50 and macd_xup:
        return "long"
    if sk < 25 and sd < 25 and rs < 50 and macd_xdn:
        return "short"
    return None
