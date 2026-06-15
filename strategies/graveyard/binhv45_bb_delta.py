#!/usr/bin/env python3
"""binhv45_bb_delta -- BinHV45 Bollinger Band Delta Dip. freqtrade berlinguyinca BinHV45.py."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "binhv45_bb_delta",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "bb_lo, bb_mid",
    "long": "sharp dip below lower BB with delta/tail ratio filter and price not rising",
    "short": "not implemented",
    "desc": "BinHV45 sharp dip below lower BB using delta and tail measurements to filter noise",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/BinHV45.py",
}


def signal(ind, pos, htf=None):
    """Sharp dip below lower BB with bbdelta / closedelta / tail filter."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    lo = ind["low"][pos]
    bbl = ind["bb_lo"][pos]
    bbl1 = ind["bb_lo"][pos - 1]
    bbm = ind["bb_mid"][pos]
    if nan(c, c1, lo, bbl, bbl1, bbm):
        return None
    if bbl1 <= 0:
        return None
    bbdelta = abs(bbm - bbl)
    closedelta = abs(c - c1)
    tail = abs(c - lo)
    if (bbdelta > c * 0.007
            and closedelta > c * 0.017
            and tail < bbdelta * 0.25
            and c < bbl1
            and c <= c1):
        return "long"
    return None
