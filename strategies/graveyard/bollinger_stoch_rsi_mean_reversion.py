#!/usr/bin/env python3
"""bollinger_stoch_rsi_mean_reversion -- BB + StochRSI extreme mean reversion. web:fmzquant."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_stoch_rsi_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, srsi_k",
    "long": "close <= bb_lo and StochRSI K below 0.1 (extreme oversold)",
    "short": "close >= bb_up and StochRSI K above 0.9 (extreme overbought)",
    "desc": "Bollinger Band + Stochastic RSI dual-confirmation extreme mean reversion",
    "source": "web:https://medium.com/@FMZQuant/bollinger-bands-mean-reversion-trading-strategy-dc80a7ff7a4f",
}

_SRSI_OB = 0.9
_SRSI_OS = 0.1


def signal(ind, pos, htf=None):
    """BB + StochRSI mean reversion."""
    c = ind["close"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    sk = ind["srsi_k"][pos]
    if nan(c, bb_lo, bb_up, sk):
        return None
    if c <= bb_lo and sk < _SRSI_OS:
        return "long"
    if c >= bb_up and sk > _SRSI_OB:
        return "short"
    return None
