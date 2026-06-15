#!/usr/bin/env python3
"""cofi_stoch_adx_ewo -- CofiBit Stoch ADX. berlinguyinca/freqtrade.

Stochastic bullish crossover below oversold threshold gated by ADX strength.
open < ema_lo13 (proxy for EMA5 of lows); ADX > 25; stoch_k crosses above stoch_d below 25.
Long-only in source; symmetric short added for FX.
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "cofi_stoch_adx_ewo",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "5m",
    "indicators": "stoch_k, stoch_d, adx, ema_lo13, ema_hi13, open",
    "long": "open < ema_lo13 AND stoch_k crosses above stoch_d AND stoch_k < 25 AND stoch_d < 25 AND adx > 25",
    "short": "open > ema_hi13 AND stoch_k crosses below stoch_d AND stoch_k > 75 AND stoch_d > 75 AND adx > 25",
    "desc": "CofiBit: stochastic oversold crossover below EMA-low with ADX strength gate",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/CofiBitStrategy.py",
}


def signal(ind, pos, htf=None):
    """Stoch crossover in oversold zone with ADX strength and EMA-band filter."""
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    dx = ind["adx"][pos]
    elo = ind["ema_lo13"][pos]
    ehi = ind["ema_hi13"][pos]
    op = ind["open"][pos]
    if nan(sk, sk1, sd, sd1, dx, elo, ehi, op):
        return None
    if op < elo and _xup(sk, sk1, sd, sd1) and sk < 25 and sd < 25 and dx > 25:
        return "long"
    if op > ehi and _xdn(sk, sk1, sd, sd1) and sk > 75 and sd > 75 and dx > 25:
        return "short"
    return None
