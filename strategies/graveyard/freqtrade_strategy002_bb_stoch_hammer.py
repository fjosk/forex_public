#!/usr/bin/env python3
"""freqtrade_strategy002_bb_stoch_hammer -- Strategy002 BB + Stochastic + Hammer (core only). freqtrade.

Hammer and Fisher RSI not in indicator set; core codeable: RSI < 30 + stoch_k < 20 + close < bb_lo
+ psar bearish (psar above price = SAR bullish flip imminent) for long.
Symmetric short: RSI > 70 + stoch_k > 80 + close > bb_up + psar bullish.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_strategy002_bb_stoch_hammer",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "5m",
    "indicators": "rsi, stoch_k, bb_lo, bb_up, psar_dir",
    "long": "rsi < 30 AND stoch_k < 20 AND close < bb_lo AND psar_dir == -1 (SAR above price)",
    "short": "rsi > 70 AND stoch_k > 80 AND close > bb_up AND psar_dir == 1 (SAR below price)",
    "desc": "Strategy002 core: RSI + Stoch + BB extreme confluence with PSAR (hammer/FisherRSI omitted)",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Strategy002.py",
}


def signal(ind, pos, htf=None):
    """RSI + Stoch + BB confluence reversal with PSAR confirmation."""
    r = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    sd = ind["psar_dir"][pos]
    c = ind["close"][pos]
    if nan(r, sk, bb_lo, bb_up, sd, c):
        return None
    # psar_dir == -1 means SAR is above price (bearish SAR placement)
    if r < 30 and sk < 20 and c < bb_lo and sd == -1:
        return "long"
    # psar_dir == 1 means SAR is below price (bullish SAR placement)
    if r > 70 and sk > 80 and c > bb_up and sd == 1:
        return "short"
    return None
