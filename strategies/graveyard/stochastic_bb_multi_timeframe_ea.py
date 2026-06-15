#!/usr/bin/env python3
"""stochastic_bb_multi_timeframe_ea -- Stochastic + BB Multi-Timeframe EA (single-TF approximation). MQL5/Sagraz.

Original requires M1+M5+M15 stochastic agreement. Approximated here on a single
timeframe using stoch_k < 20 + bb_lo breach + rsi < 30 for long (all oversold); mirror
for short. This captures the confluence intent without a true multi-TF read.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_bb_multi_timeframe_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "stoch_k, stoch_d, bb_up, bb_lo, rsi",
    "long": "stoch_k < 20 AND stoch_d < 20 AND close < bb_lo AND rsi < 30",
    "short": "stoch_k > 80 AND stoch_d > 80 AND close > bb_up AND rsi > 70",
    "desc": "Stochastic + BB + RSI oversold/overbought confluence (single-TF approximation of MTF EA)",
    "source": "web:https://www.mql5.com/en/code/58746",
}


def signal(ind, pos, htf=None):
    """Stochastic + BB + RSI confluence reversal."""
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    if nan(sk, sd, bb_lo, bb_up, r, c):
        return None
    if sk < 20 and sd < 20 and c < bb_lo and r < 30:
        return "long"
    if sk > 80 and sd > 80 and c > bb_up and r > 70:
        return "short"
    return None
