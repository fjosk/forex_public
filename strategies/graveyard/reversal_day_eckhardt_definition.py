#!/usr/bin/env python3
"""reversal_day_eckhardt_definition -- Eckhardt's geometric reversal day: new extreme then reversal close. the_new_market_wizards.

Bearish reversal day: today makes a new N-bar high AND closes below yesterday's close.
Bullish reversal day: today makes a new N-bar low AND closes above yesterday's close.
Eckhardt notes this has near-zero standalone expectancy; included as a systematic test.
N-bar high/low via hh_n/ll_n indicator.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "reversal_day_eckhardt_definition",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,low,close,hh_n,ll_n",
    "long": "New N-bar low (ll_n) AND close > prior close -> bullish reversal day",
    "short": "New N-bar high (hh_n) AND close < prior close -> bearish reversal day",
    "desc": "Eckhardt reversal day: new extreme that closes against the trend (near-zero standalone expectancy per source)",
    "source": "book:the_new_market_wizards",
}


def signal(ind, pos, htf=None):
    """Eckhardt reversal day: new high/low bar that closes in the opposite direction."""
    if pos < 1:
        return None
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    hhn = ind["hh_n"][pos]
    lln = ind["ll_n"][pos]
    if nan(h[pos], lo[pos], c[pos], c[pos-1], hhn, lln):
        return None

    # Bearish reversal day: new high, close below prior close
    if h[pos] >= hhn and c[pos] < c[pos-1]:
        return "short"

    # Bullish reversal day: new low, close above prior close
    if lo[pos] <= lln and c[pos] > c[pos-1]:
        return "long"

    return None
