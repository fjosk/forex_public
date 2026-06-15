#!/usr/bin/env python3
"""freqtrade_bbband_rsi_stoch_hammer -- Freqtrade Bollinger RSI Stochastic Reversal Strategy002."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_bbband_rsi_stoch_hammer",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, stoch_k, bb_lo, psar_dir",
    "long": "rsi < 30 AND stoch_k < 20 AND close < bb_lo",
    "short": "not implemented (long only)",
    "desc": "Triple oversold confirmation: RSI + slow stochastic + below lower BB; PSAR for exit",
    "source": "github.com/freqtrade/freqtrade-strategies Strategy002.py",
}


def signal(ind, pos, htf=None):
    """Three-way oversold: RSI < 30, stoch_k < 20, close < bb_lo."""
    c = ind["close"][pos]
    r = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    bbl = ind["bb_lo"][pos]
    if nan(c, r, sk, bbl):
        return None
    if r < 30 and sk < 20 and c < bbl:
        return "long"
    return None
