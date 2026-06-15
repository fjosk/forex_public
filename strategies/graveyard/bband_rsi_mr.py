#!/usr/bin/env python3
"""bband_rsi_mr -- Bollinger Band RSI Mean Reversion. freqtrade berlinguyinca BbandRsi."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bband_rsi_mr",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, bb_lo",
    "long": "rsi < 30 AND close < bb_lo",
    "short": "not implemented (long only)",
    "desc": "Classic oversold bounce: price below lower BB and RSI oversold",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/BbandRsi.py",
}


def signal(ind, pos, htf=None):
    """RSI oversold + price below lower Bollinger Band."""
    c = ind["close"][pos]
    r = ind["rsi"][pos]
    bbl = ind["bb_lo"][pos]
    if nan(c, r, bbl):
        return None
    if r < 30 and c < bbl:
        return "long"
    return None
