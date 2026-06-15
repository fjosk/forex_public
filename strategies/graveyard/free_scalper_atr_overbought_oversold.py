#!/usr/bin/env python3
"""free_scalper_atr_overbought_oversold -- OR-logic scalper: RSI/Stoch/BB overbought-oversold on M5.

No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "free_scalper_atr_overbought_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "rsi, stoch_k, bb_lo, bb_up, close",
    "long": "rsi<30 OR stoch_k<20 OR close<bb_lo",
    "short": "rsi>70 OR stoch_k>80 OR close>bb_up",
    "desc": "Conservative scalper: OR of RSI/Stoch/BB oversold for long, overbought for short",
    "source": "github.com/ersingencturk/FreeExpertAdvisor M5 scalper",
}


def signal(ind, pos, htf=None):
    """OR-logic overbought/oversold scalp signal."""
    rs = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    cl = ind["close"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    if nan(rs, sk, cl, bb_lo, bb_up):
        return None
    if rs < 30 or sk < 20 or cl < bb_lo:
        return "long"
    if rs > 70 or sk > 80 or cl > bb_up:
        return "short"
    return None
