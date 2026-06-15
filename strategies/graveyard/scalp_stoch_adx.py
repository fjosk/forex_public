#!/usr/bin/env python3
"""scalp_stoch_adx -- Open below EMA-low, ADX>30, stochastic oversold crossover (berlinguyinca Scalp).

ema_lo13 (13-period EMA of lows) approximates EMA(5, lows). Long-only per source.
No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, _xup, ALL_CLASSES

META = {
    "id": "scalp_stoch_adx",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "ema_lo13, adx, stoch_k, stoch_d",
    "long": "open < ema_lo13 AND adx>30 AND stoch_k<30 AND stoch_d<30 AND stoch_k crosses above stoch_d",
    "short": "not implemented (source is long-only)",
    "desc": "Stochastic+ADX scalp: dip below EMA-low confirmed by ADX strength and stochastic cross",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/Scalp.py",
}


def signal(ind, pos, htf=None):
    """Stochastic+ADX dip scalp: long only."""
    if pos < 1:
        return None
    elo = ind["ema_lo13"][pos]
    dx = ind["adx"][pos]
    sk0 = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd0 = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    op = ind["open"][pos]
    if nan(elo, dx, sk0, sk1, sd0, sd1, op):
        return None
    stoch_cross_up = _xup(sk0, sk1, sd0, sd1)
    if op < elo and dx > 30 and sk0 < 30 and sd0 < 30 and stoch_cross_up:
        return "long"
    return None
