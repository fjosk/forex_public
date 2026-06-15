#!/usr/bin/env python3
"""freqtrade_bbband_rsi -- Freqtrade BbandRsi Bollinger + RSI Mean Reversion. berlinguyinca."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_bbband_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, bb_lo",
    "long": "rsi < 30 AND close < bb_lo",
    "short": "not implemented (long only)",
    "desc": "Simplest double-condition mean reversion baseline: RSI oversold + below lower BB",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/BbandRsi.py",
}


def signal(ind, pos, htf=None):
    """RSI < 30 AND close below lower Bollinger Band."""
    c = ind["close"][pos]
    r = ind["rsi"][pos]
    bbl = ind["bb_lo"][pos]
    if nan(c, r, bbl):
        return None
    if r < 30 and c < bbl:
        return "long"
    return None
