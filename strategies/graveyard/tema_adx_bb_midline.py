#!/usr/bin/env python3
"""tema_adx_bb_midline -- TEMA9 below BB mid, rising, ADX strong, price below SMA200. freqtrade/berlinguyinca.

Dip-in-downtrend setup: price and TEMA below SMA200 and BB midline, but TEMA rising with ADX.
Long-only entry from the Quickie strategy.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "tema_adx_bb_midline",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h",
    "indicators": "tema9, adx, bb_mid, sma200",
    "long": "ADX > 30 AND tema9 < bb_mid AND tema9 rising AND close < sma200",
    "short": "Not implemented (long-only reversal from depressed trend)",
    "desc": "TEMA9 dip below BB midline with ADX strength, below SMA200",
    "source": "https://github.com/freqtrade/freqtrade-strategies berlinguyinca/Quickie.py",
}


def signal(ind, pos, htf=None):
    """TEMA9 below BB mid and rising, ADX strong, price below SMA200."""
    t = ind["tema9"][pos]
    t1 = ind["tema9"][pos - 1]
    a = ind["adx"][pos]
    bm = ind["bb_mid"][pos]
    ma200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(t, t1, a, bm, ma200, c):
        return None
    if a > 30 and t < bm and t > t1 and ma200 > c:
        return "long"
    return None
